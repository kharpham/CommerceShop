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
  $(".filter-checkbox, #price-filter-button").on("click", function () {
    let filterObject = {};
    let min_price = $("#max_price").attr("min");
    let max_price = $("#max_price").val();
    filterObject.min_price = min_price;
    filterObject.max_price = max_price;

    $(".filter-checkbox").each(function () {
      let filterKey = $(this).data("filter");
      filterObject[filterKey] = Array.from(
        document.querySelectorAll(
          "input[data-filter=" + filterKey + "]:checked"
        )
      ).map(function (element) {
        return element.value;
      });
    });
    $.ajax({
      url: "/filtered-products",
      data: filterObject,
      dataType: "json",
      beforeSend: function () {
        console.log("Filtering products...");
      },
      success: function (response) {
        console.log(response);
        $("#filtered-products").html(response.data);
        $("#product-count").text(response.product_count);
        console.log("Data filtered successfully...");
      },
    });
  });

  $("#max_price").on("blur", function () {
    let min_price = $(this).attr("min");
    let max_price = $(this).attr("max");
    let current_price = $(this).val();
    console.log("Value is", current_price);
    console.log("Min Value is", min_price);
    console.log("Max Value is", max_price);

    if (current_price < min_price || current_price > max_price) {
      alert("Price must be between $" + min_price + " and $" + max_price);
      $(this).val(min_price);
      $(this).focus();
      $("#range").val(min_price);
      return false;
    }
  });
});

// Add to cart
$(".add-to-cart-button").on("click", function () {
  let thisVal = $(this);
  let _index = thisVal.attr("data-index");
  let quantity = $(".product-quantity-" + _index).val();
  let productTitle = $(".product-title-" + _index).val();
  let productPid = $(".product-pid-" + _index).val();
  let productPrice = $(".current-product-price-" + _index).text();
  let productImage = $(".product-image-" + _index).val();
  console.log("Quantity", quantity);
  console.log(productTitle);
  console.log(productPid);
  console.log(productPrice);
  console.log(productImage);

  $.ajax({
    url: "/add-to-cart",
    data: {
      pid: productPid,
      quantity: quantity,
      title: productTitle,
      price: productPrice,
      image: productImage,
    },
    dataType: "json",
    beforeSend: function () {
      console.log("Adding product to Cart...");
    },
    success: function (response) {
      thisVal.html("✔");
      console.log("Product added to Cart successfully...");
      $(".cart-items-count").text(response.total_cart_items);
    },
  });
});

// Delete cart item
$(".delete-product").on("click", function () {
  let pid = $(this).data("product");
  $.ajax({
    url: "/remove-from-cart",
    data: {
      pid,
    },
    dataType: "json",
    beforeSend: function () {
      console.log("Removing product from Cart...");
    },
    success: function (response) {
      console.log("Product removed from Cart successfully...");
      if (response.data.product_amount > 0) {
        $("#product-" + pid).remove();
        $("#cart-subtotal-amount").text(
          "$" + response.data.cart_total_amount.toFixed(2)
        );
        $("#cart-total-amount").text(
          "$" + response.data.cart_total_amount.toFixed(2)
        );
        $("#product-amount").text(response.data.product_amount);
        $(".cart-product-count").text(response.data.product_amount);
      } else {
        $("#cart-table").remove();
        $("#cart-bill").remove();
        $("#product-amount").text(response.data.product_amount);
        $(".cart-product-count").text(response.data.product_amount);
      }
    },
  });
});

// Update cart item
$(".refresh-product").on("click", function () {
  let pid = $(this).data("product");
  console.log(pid);
  let quantity = $("#product-quantity-" + pid).val();
  console.log(quantity);
  $.ajax({
    url: "/update-cart",
    dataType: 'json',
    data: {
      pid,
      quantity,
    },
    beforeSend: function () {
      console.log("Updating product...");
    },
    success: function (response) {
      $("#product-subtotal-" + pid).text(
        "$" + response.data.product_subtotal.toFixed(2)
      );
      $("#cart-subtotal-amount").text(
        "$" + response.data.cart_total_amount.toFixed(2)
      );
      $("#cart-total-amount").text(
        "$" + response.data.cart_total_amount.toFixed(2)
      );
      console.log("Product updated successfully...");
    },
  });
});

// Download invoice
$("#invoice_download_btn").on("click", function () {
  console.log("Downloading...");
  const { jsPDF } = window.jspdf;

  let doc = new jsPDF("1", "mm", [1600, 1400]);
  let pdfjs = document.querySelector("#invoice_wrapper");
  doc.html(pdfjs, {
    callback: function (doc) {
      doc.save("invoice.pdf");
    },
    x: 30,
    y: 30,
  });
});

// Make address default
$(".make-default").on("click", function () {
  let address_id = $(this).attr("id");
  let button = $(this);

  $.ajax({
    url: "/default-address",
    dataType: "json",
    data: {
      address_id,
    },
    beforeSend: function () {
      console.log("Updating address...");
    },
    success: function (response) {
      if (response.data["undefault"] != "None") {
        button.hide();
        $("#address-" + address_id).show();
        $("#" + response.data["undefault"]).show();
        $("#address-" + response.data["undefault"]).hide();
        console.log("Address updated successfully...");
      }
      else {
        button.hide();
        $("#address-" + address_id).show();
      }
    },
  });
});

// Add product to wishlist
 $(".add-to-wishlist").on("click", function() {
  let product_pid = $(this).data("index");
  let button = $(this);
  $.ajax({
    url: '/add-to-wishlist',
    data: {
      product_pid,
    },
    beforeSend: function() {
      console.log("Adding product to wishlist...");
    },
    success: function(response) {
      // button.removeClass('add-to-wishlist');
      // button.addClass('remove-from-wishlist');
      // $("#add-remove-icon-" + product_pid).css("color", "red");
      button.hide()
      $("#remove-button-" + product_pid).show();
      $("#wishlist-count").text(response.wishlist_amount);
      console.log(response.message);
    }
  })
 });

 // Remove product from wishlist
 $(".remove-from-wishlist").on("click", function() {
  let product_pid = $(this).data("index");
  let button = $(this);
  $.ajax({
    url: '/remove-from-wishlist',
    data: {
      product_pid,
    },
    beforeSend: function() {
      console.log("Removing product to wishlist...");
    },
    success: function(response) {
      // button.removeClass('remove-from-wishlist');
      // button.addClass('add-to-wishlist');
      // $("#add-remove-icon-" + product_pid).css("color", "grey");
      button.hide()
      $("#add-button-" + product_pid).show();
      $("#wishlist-count").text(response.wishlist_amount);
      console.log(response.message);
    }
  })
 });

