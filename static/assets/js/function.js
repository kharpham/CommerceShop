console.log("ajax-add-review");

$("#commentForm").submit(function(event) {
  event.preventDefault();
  $.ajax({
    data: $(this).serialize(),
    method: $(this).attr("method"),
    url: $(this).attr("action"),
    dataType: "json",
    success: (response) => {
      console.log("Comment Saved to Db");

      if (response.bool == true) {
        $("#review-response").html("Review Added Successfully");
      }
      else {
        alert("Comment not saved");
      }
    },
    error: (xhr, status, error) => {
      console.log("Error occured", error);
    },
  });
});
