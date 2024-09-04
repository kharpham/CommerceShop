$("#commentForm").submit(function (event) {
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
        $(".hide-comment-form").hide();
        $(".hide-comment-title").hide();

        let _html =
          '<div class="single-comment justify-content-between d-flex mb-30">';
        _html += "<div";
        _html += ' class="user justify-content-between d-flex"';
        _html += ">";
        _html += '<div class="thumb text-center">';
        _html += "<img";
        _html +=
          ' src="https://th.bing.com/th/id/OIP.PoS7waY4-VeqgNuBSxVUogAAAA?rs=1&pid=ImgDetMain"';
        _html += ' alt=""';
        _html += "/>";
        _html += '<a href="#" class="font-heading text-brand"';
        _html += ">" + response.context.user + "</a";
        _html += ">";
        _html += "</div>";
        _html += '<div class="desc">';
        _html += "<div";
        _html += ' class="d-flex justify-content-between mb-10"';
        _html += ">";
        _html += '<div class="d-flex align-items-center">';
        _html += '<span class="font-xs text-muted">';
        _html += response.date;
        _html += "</span>";
        _html += "</div><span>";
        for (let i = 0; i < response.context.rating; i++) {
          _html += '<i class="fas fa-star text-warning"></i>';
        }
        _html += "</span></div>";
        _html += '<p class="mb-10">';
        _html += response.context.review;
        _html += "</p>";
        _html += "</div>";
        _html += "</div>";
        _html += "</div>";

        $(".comment-list").prepend(_html);
      } else {
        alert("There is an error saving the review");
      }
    },
    error: (xhr, status, error) => {
      alert("There is an error saving the review");
    },
  });
});

$(document).ready(function () {
  $(".filter-checkbox").on("click", function () {
    let filterObject = {};
    $(".filter-checkbox").each(function () {
      let filterKey = $(this).data("filter");
      filterObject[filterKey] = (Array.from(
        document.querySelectorAll(
          "input[data-filter=" + filterKey + "]:checked"
        )).map(function(element) {
          return element.value;
        })
      );
    });
    $.ajax({
      url: '/filtered-products',
      data: filterObject,
      dataType: 'json',
      beforeSend: function() {
        console.log("Filtering products...");
      },
      success: function(response) {
        console.log(response);
        $("#filtered-products").html(response.data);
        $("#product-count").text(response.product_count);
        console.log("Data filtered successfully...");
      }
    })
  });
});
