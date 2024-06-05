package org.parasol.resources;

import java.util.List;

import org.parasol.model.Claim;

import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.PathParam;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;

@Produces(MediaType.APPLICATION_JSON)
@Path("/api/db/claims")
public class ClaimResource {

    @GET
    public List<Claim> getall() {
        return Claim.listAll();
    }

    @GET
    @Path("/{id}")
    public Claim getone(@PathParam("id") int id) {
        return Claim.findById(id);
    }
}
