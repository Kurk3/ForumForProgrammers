function like(postId) {
    var likeCount = document.getElementById("likes-count-".concat(postId));
    var likeButton = document.getElementById("like-button-".concat(postId));
    fetch("/like-post/".concat(postId), { method: "POST" })
        .then(function (res) { return res.json(); })
        .then(function (data) {
        likeCount.innerHTML = data["likes"];
        if (data["liked"] === true) {
            likeButton.className = "fas fa-thumbs-up";
        }
        else {
            likeButton.className = "far fa-thumbs-up";
        }
    })["catch"](function (e) { return alert("Could not like post."); });
}
