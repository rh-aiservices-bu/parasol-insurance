import psycopg2
from psycopg2.extras import RealDictCursor
import sys
import logging

class Database:
    def __init__(self, config, logger):
        self.logger = logger
        self.conn = self.connect(config)
        
    def connect(self, config):
            """
            Connect to the PostgreSQL database using the provided configuration and return the connection object.

            Args:
                config (dict): A dictionary containing the configuration parameters for the database connection.

            Returns:
                conn (psycopg2.extensions.connection): A connection object representing the database connection.
            """
            self.logger.info(f"Connecting to PostgreSQL Database...")
            try:
                conn = psycopg2.connect(
                        host = config["POSTGRES_HOST"],
                        dbname = config["POSTGRES_DB"],
                        user = config["POSTGRES_USER"],
                        password = config["POSTGRES_PASSWORD"],
                        port = config["POSTGRES_PORT"]
                    )
                self.logger.info(f"Connection successful!")
            except psycopg2.OperationalError as e:
                self.logger.info(f"Could not connect to Database: {e}")

            return conn

    def list_tables(self):
        """
        Returns a list of table names in the 'claims' schema of the database.
        """
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute("SELECT tablename from pg_catalog.pg_tables WHERE schemaname='claims';")
            result = cur.fetchall()
            self.conn.commit()
            return result
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cur.close()

    def list_claims(self):
        """
        Returns a list of all claims in the database.

        Returns:
        list: A list of dictionaries representing each claim, with keys 'id' and 'subject'.
        """
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            query = """
            SET schema 'claims';
            SELECT claims.id, claims.claim_number, claims.category, claims.policy_number, claims.client_name, claims.subject, claims.summary
            FROM claims
            ORDER BY claims.id
            """
            cur.execute(query)
            result = cur.fetchall()
            self.conn.commit()
            return result
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cur.close()

    def list_claims_unprocessed(self):
        """
        Returns a list of all claims in the database that have an empty summary.

        Returns:
        list: A list of dictionaries representing each claim, with keys 'id' and 'subject'.
        """
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            query = """
            SET schema 'claims';
            SELECT claims.id, claims.subject
            FROM claims
            WHERE claims.summary IS NULL OR claims.summary = ''
            """
            cur.execute(query)
            result = cur.fetchall()
            self.conn.commit()
            return result
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cur.close()
        
    def get_claim_base_info(self, claim_id):
        """
        Retrieves base information about a claim from the database.

        Args:
            claim_id (int): The ID of the claim to retrieve.

        Returns:
            dict: A dictionary containing information about the claim, including its ID, subject, and summary.

        Example:
            {
                "id": 1,
                "subject": "Car accident",
                "summary": "I was involved in a car accident on the highway.",
            }
        """
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            query = """
            SET schema 'claims';
            SELECT claims.id, claims.subject, claims.summary
            FROM claims WHERE claims.id = %s;
            """
            cur.execute(query, (claim_id,))
            result = cur.fetchone()
            self.conn.commit()
            return result
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cur.close()

    def get_claim_info(self, claim_id):
        """
        Retrieves information about a claim from the database.

        Args:
            claim_id (int): The ID of the claim to retrieve.

        Returns:
            dict: A dictionary containing information about the claim, including its ID, subject, body, sentiment, and images.

        Example:
            {
                "id": 1,
                "subject": "Car accident",
                "body": "I was involved in a car accident on the highway.",
                "sentiment": "positive",
                "location": "New York",
                "time": "2020-10-10 10:10:10",
                "original_images": [
                    {"image_name": "image1.jpg", "image_key": "key1"},
                    {"image_name": "image2.jpg", "image_key": "key2"}
                ],
                "processed_images": [
                    {"image_name": "image1.png", "image_key": "key1"},
                    {"image_name": "image2.png", "image_key": "key2"}
                ]
            }
        """
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            query = """
            SET schema 'claims';
            SELECT claims.id, claims.claim_number, claims.category, claims.policy_number, claims.client_name, claims.subject, claims.body, claims.sentiment, claims.summary, claims.location, claims.time,
            (SELECT json_agg(
                json_build_object('image_name',original_images.image_name,'image_key',original_images.image_key)) AS original_images
            FROM original_images WHERE claim_id = claims.id
            ),
            (SELECT json_agg(
                json_build_object('image_name',processed_images.image_name,'image_key',processed_images.image_key)) AS processed_images
            FROM processed_images WHERE claim_id = claims.id
            )
            FROM claims WHERE claims.id = %s;
            """
            cur.execute(query, (claim_id,))
            result = cur.fetchone()
            self.conn.commit()
            return result
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cur.close()

    def create_claim(self, subject, body):
        """
        Creates a new claim in the database.

        Args:
            subject (str): The subject of the claim.
            body (str): The body of the claim.

        Returns:
            int: The ID of the claim that was created.
        """
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            query = """
            SET schema 'claims';
            INSERT INTO claims (subject, body) VALUES (%s, %s) RETURNING id;
            """
            cur.execute(query, (subject, body))
            result = cur.fetchone()
            self.conn.commit()
            return result["id"]
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cur.close()

    def update_claim_summary(self, claim_id, summary):
        """
        Updates the summary of a claim in the database.

        Args:
            claim_id (int): The ID of the claim to update.
            summary (str): The summary to update the claim with.
        """
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            query = """
            SET schema 'claims';
            UPDATE claims SET summary = %s WHERE id = %s;
            """
            cur.execute(query, (summary, claim_id))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cur.close()

    def update_claim_location(self, claim_id, location):
        """
        Updates the location of a claim in the database.

        Args:
            claim_id (int): The ID of the claim to update.
            location (str): The location to update the claim with.
        """
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            query = """
            SET schema 'claims';
            UPDATE claims SET location = %s WHERE id = %s;
            """
            cur.execute(query, (location, claim_id))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cur.close()

    def update_claim_time(self, claim_id, time):
        """
        Updates the time of a claim in the database.

        Args:
            claim_id (int): The ID of the claim to update.
            time (str): The time to update the claim with.
        """
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            query = """
            SET schema 'claims';
            UPDATE claims SET time = %s WHERE id = %s;
            """
            cur.execute(query, (time, claim_id))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cur.close()

    def update_claim_body(self, claim_id, body):
        """
        Updates the body of a claim in the database.

        Args:
            claim_id (int): The ID of the claim to update.
            body (str): The body to update the claim with.
        """
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            query = """
            SET schema 'claims';
            UPDATE claims SET body = %s WHERE id = %s;
            """
            cur.execute(query, (body, claim_id))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cur.close()

    def update_claim_subject(self, claim_id, subject):
        """
        Updates the subject of a claim in the database.

        Args:
            claim_id (int): The ID of the claim to update.
            subject (str): The subject to update the claim with.
        """
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            query = """
            SET schema 'claims';
            UPDATE claims SET subject = %s WHERE id = %s;
            """
            cur.execute(query, (subject, claim_id))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cur.close()

    def update_claim_sentiment(self, claim_id, sentiment):
        """
        Updates the sentiment of a claim in the database.

        Args:
            claim_id (int): The ID of the claim to update.
            sentiment (str): The sentiment to update the claim with.
        """
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            query = """
            SET schema 'claims';
            UPDATE claims SET sentiment = %s WHERE id = %s;
            """
            cur.execute(query, (sentiment, claim_id))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cur.close()

    def delete_claim(self, claim_id):
        """
        Deletes a claim from the database.

        Args:
            claim_id (int): The ID of the claim to delete.
        """
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            query = """
            SET schema 'claims';
            DELETE FROM claims WHERE id = %s;
            """
            cur.execute(query, (claim_id,))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cur.close()

    def upload_original_image(self, claim_id, image_name, image_key):
        """
        Creates a new original image in the database.

        Args:
            claim_id (int): The ID of the claim the image belongs to.
            image_name (str): The name of the image.
            image_key (str): The key of the image.
        """
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            query = """
            SET schema 'claims';
            INSERT INTO original_images (claim_id, image_name, image_key) VALUES (%s, %s, %s);
            """
            cur.execute(query, (claim_id, image_name, image_key))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cur.close()

    def upload_processed_image(self, claim_id, image_name, image_key):
        """
        Creates a new processed image in the database.

        Args:
            claim_id (int): The ID of the claim the image belongs to.
            image_name (str): The name of the image.
            image_key (str): The key of the image.
        """
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            query = """
            SET schema 'claims';
            INSERT INTO processed_images (claim_id, image_name, image_key) VALUES (%s, %s, %s);
            """
            cur.execute(query, (claim_id, image_name, image_key))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cur.close()

    def delete_original_image(self, claim_id, image_key):
        """
        Deletes an original image from the database.

        Args:
            claim_id (int): The ID of the claim the image belongs to.
            image_key (str): The key of the image.
        """
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            query = """
            SET schema 'claims';
            DELETE FROM original_images WHERE claim_id = %s AND image_key = %s;
            """
            cur.execute(query, (claim_id, image_key))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cur.close()

    def delete_processed_image(self, claim_id, image_key):
        """
        Deletes a processed image from the database.

        Args:
            claim_id (int): The ID of the claim the image belongs to.
            image_key (str): The key of the image.
        """
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            query = """
            SET schema 'claims';
            DELETE FROM processed_images WHERE claim_id = %s AND image_key = %s;
            """
            cur.execute(query, (claim_id, image_key))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cur.close()
    
