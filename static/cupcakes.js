/** Use relative URLs for accessing Flask routes to bypass data retrieval errors with CORs */
const BASE_API_URL = "/api";

/** Dynamically generate cupcake html from server Cupcake object */

function generateCupcakes(cupcake){
    const cupcake_HTML = `
        <div data-cupcake-id=${cupcake.id}>

            <li>
                ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
                <button id="delete-button">X</button> 
            </li>

            <img style="max-width: 200px; max-height: 200px;"
                src="${cupcake.image}"
                alt="Image of ${cupcake.size}, ${cupcake.flavor} cupcake with rating of ${cupcake.rating}.">

        </div>`;

    return cupcake_HTML;
}

/** Generate initial cupcakes from database on page */

async function showCupcakes(){
    
    const resp = await axios.get(`${BASE_API_URL}/cupcakes`);
    
    for (let cupcakeData of resp.data.cupcakes){
        let newCupcake = $(generateCupcakes(cupcakeData));
        $("#cupcakes-list").append(newCupcake);
    }
}

/** form handling for adding new cupcakes */

$("#add-cupcake-form").on("submit", async function(evt){
    evt.preventDefault();
  
    let flavor = $("#cupcake-flavor").val();
    let size = $("#cupcake-size").val();
    let rating = $("#cupcake-rating").val();
    let image = $("#cupcake-image").val();
  
    const newCupcakeResp = await axios.post(`${BASE_API_URL}/cupcakes`, {flavor, size, rating, image});
  
    let newCupcake = $(generateCupcakes(newCupcakeResp.data.cupcake));
    $("#cupcakes-list").append(newCupcake);
    $("#add-cupcake-form").trigger("reset");
});

/** handle deleting cupcakes */

$("#cupcakes-list").on("click", "#delete-button", async function(evt) {
    evt.preventDefault();

    let $cupcake = $(evt.target).closest("div");
    let cupcakeId = $cupcake.attr("data-cupcake-id");
  
    await axios.delete(`${BASE_API_URL}/cupcakes/${cupcakeId}`);
    $cupcake.remove();

});
  
$(showCupcakes);