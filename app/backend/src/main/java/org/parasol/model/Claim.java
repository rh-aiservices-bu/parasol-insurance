package org.parasol.model;

import io.quarkus.hibernate.orm.panache.PanacheEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;

@Entity
public class Claim extends PanacheEntity {

    public String claim_number;
    public String category;
    public String policy_number;
    public String client_name;
    public String subject;
    @Column(length = 5000)
    public String body;
    @Column(length = 5000)
    public String summary;
    public String location;
    @Column(name = "claim_time")
    public String time;
    @Column(length = 5000)
    public String sentiment;

}
