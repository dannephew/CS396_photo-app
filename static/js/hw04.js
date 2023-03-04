const story2Html = story => {
    return `
        <div>
            <img src="${ story.user.thumb_url }" class="pic" alt="profile pic for ${ story.user.username }" />
            <p>${ story.user.username }</p>
        </div>
    `;
};

const user2Html = user => {
    return `
        <div>
            <img src="${ user.thumb_url }" />
            <p>${ user.username }</p>
        </div>
    `
}

const suggestions2Html = suggestion => {
    return `
    <img src="${ suggestion.thumb_url }" />
    <p>${ suggestion.username }</p>
    <p>Suggested for you</p>
    <button>Follow</button>
    `
}

const comments2Html = comment => {
return `

    `;

};

// fetch data from your API endpoint:
const displayStories = () => {
    console.log("displayStories")
    fetch('/api/stories')
        .then(response => response.json())
        .then(stories => {
            const html = stories.map(story2Html).join('\n');
            document.querySelector('.stories').innerHTML = html;
        })
};
//get post data from API endpoint (/api/posts?limit-10)
//when data arrives (after promises), build a bunch of HTML nested elements that become cards (i.e. a long string)
//update the container and put the HTML inside it 

{/* <section id = "posts">
    <div id="post_top">
        <h2>${ post.user.username}</h2>
        <h4>•••</h4>
    </div>
    <img src=${ post.image_url} id="post_pic" alt="post image of ${post.user.username}"/>
    <section class="post_bottom">
        <section>
            <div id = "post_icons">
                <div>
                    <i class="far fa-heart"></i>
                    <i class="far fa-comment"></i>
                    <i class="far fa-paper-plane"></i>
                </div>
                <i class="far fa-bookmark"></i>
            </div>
            <section id="post_descrip">
                <div class="post_descrip_div" id="likes">
                    <h4 id="post_words" class="name">${ post.likes.length} likes</h4>
                </div>
                <div class="post_descrip_div">
                    <h5 class = "name" id="post_words">{{ c.get('user').get('username') }}</h5>
                    <h5 id="post_words"> {{ c.get('title') }} </h5>
                </div>
                
                ${ post.comments.length > 1 ?                     <h5 id="post_words"><a href="more">View all ${post.comments.length} comments</a></h5> 
                    : post.comments.length >= 1 ? 
                    for comment in post.comments: 
                       <div class="post_descrip_div">
                        <h5 class = "name" id="post_words">${comment.user.username}</h5>
                       <h5 id="post_words"> ${ comment.text}</h5>
                </div>    
                    }

                {% endif %}

                {% if c.get('comments')|length >= 1 %}
                <div class="post_descrip_div">
                    <h5 class = "name" id="post_words">{{ c.get('comments')[0].get('user').get('username')}}</h5>
                    <h5 id="post_words"> {{ c.get('comments')[0].get('text')}}</h5>
                </div>                
                {% endif %}

                <div class="post_descrip_div">
                    <h5 id="post_words">{{ c.get('display_time') }}</h5>
                </div>
            </section>

        </section>

        <section id="new_comment">
            <div id=new_comment_left>
                <i class="far fa-smile"></i>
                <h4 id = "new_comment_left_words">Add a comment...</h4>
            </div>
            <div>
                <h4>Post</h4>
            </div>
        </section>
    </section>
</section> */}

const post2Html = post => {
    console.log("post2Html")
    return `
    <section id = "posts">
    <div id="post_top">
        <h2>${ post.user.username} - ${post.current_user_like_id} - ${post.current_user_bookmark_id}</h2>
        <h4>•••</h4>
    </div>
    <img src=${ post.image_url} id="post_pic" alt="post image of ${post.user.username}"/>
    <section class="post_bottom">
            <div id = "post_icons">
                <div>
                    <button class="like" onclick="toggleLike(${post.id}, ${post.current_user_like_id})"><i class="fa${ post.current_user_like_id ? 's' : 'r'} fa-heart"></i></button>
                    <i class="far fa-comment"></i>
                    <i class="far fa-paper-plane"></i>
                </div>
                ${  renderBookmarkButton(post)  }
            </div>
        <div>
            <p>${ post.caption }</p>
        </div>
        <div class="post_descrip_div" id="likes">
        <h4 id="post_words" class="name">${ post.likes.length} like${post.likes.length != 1 ? 's' : ''}</h4>
        <div class="modal-bg">${ getCommentButton(post) }</div>
        
        </section>
    </section>
    `;
};

//
const modalElement = document.querySelector('.modal-bg');

const openModal = ev => {
    console.log("open!")
}

const closeModal = ev => {
    console.log("close!")
}

const getCommentButton = (post) => {
    if (post.comments.length > 1) {
        return `
        <button>View ${post.comments.length} Comments</button>
        <p>${ post.comments[post.comments.length-1].text }</p>
        `
    } else if (post.comments.length == 1){
        return `
        <p>${ post.comments[0].text }</p>
        `
    } else {
        return ``
    }

}

const toggleLike = (postid, like_id) => {
    //has this already been liked
    if (like_id == null){
        console.log(postid)
        const url = `/api/posts/${postid}/likes/` 
        console.log(url)

        fetch(url, {method: 'POST'})
        //tell server we're using post request, not get request
        .then(response => response.json())
        .then(like => {
            console.log(like)

            //requery server for POST
            /////redraw the post -- do we need to do this without reloading page?
            //document.querySelector
        })}
    else{
        console.log("You've already liked this. Delete like")
        const url = `/api/posts/${postid}/likes/${like_id}` 
        fetch(url, {method: 'DELETE'})
        //tell server we're using post request, not get request
        .then(response => response.json())
        .then(like => {
            console.log(like)
            /////redraw the post -- do we need to do this without reloading page?
            
        })
    }
        

}
// Issue post request
// Then it responds, but post object is not in sync
// Actually has more likes
//Must requery and get fresh copy of post object
//invoke post2html
const renderLikeButton = post => {
    if (post.current_user_like_id) {
        `
        <button
            data-like-id="${post.current_user_like_id}"
            data-post-id="${post.id}"
            aria-label="Like / Unlike"
            aria-checked="true"
            onclick="handleLike(event);">
            <i class ="fas fa-heart"></i>
            </button>
        `;
    } else {
        return `
        <button
            data-post-id="${post.id}"
            aria-label="Like / Unlike"
            aria-checked="false"
            onclick="handleLike(event);">
            <i class ="far fa-heart"></i>
            </button>
        `;
    }
}

const renderBookmarkButton = post => {
    if (post.current_user_bookmark_id) {
        return `
        <button
            data-post-id="${post.id}"
            data-bookmark-id="${post.current_user_bookmark_id}"
            aria-label="Bookmark / Unbookmark"
            aria-checked="true"
            onclick="handleBookmark(event);">
            <i class="fas fa-bookmark"></i>
        </button>
        `
    } else {
        return `
        <button
            data-post-id="${post.id}"
            aria-label="Bookmark / Unbookmark"
            aria-checked="false"
            onclick="handleBookmark(event);">
            <i class="far fa-bookmark"></i>
        </button>
        `
    }
    //if bookmark has been liked, then unlike
    //if bookmark has been unliked, then like
}

const handleLike = ev => {
    console.log("Handle like functionality")
    // if area-checked == 'true' then Delete Like Object
    //else: Issue a POST request to create a Like Object
}

const handleBookmark = ev => {
    console.log("Handle bookmark functionality")
}

const toggleFollow = (INSERT) => {
    //if account is currently being followed, then unfollow
    //if account is currently not followed, then follow

}

const displayPosts = () => {
    console.log("displayPosts")
    fetch('/api/posts')
        .then(response => response.json())
        .then(posts => {
            const html = posts.map(post2Html).join('\n');
            document.querySelector('#posts').innerHTML = html;
        })
};

const displayUserProfile = () => {
    fetch('/api/profile')
        .then(response => response.json())
        .then(user => {
            const html = user2Html(user);
            console.log(html)
            document.querySelector('.user-profile').innerHTML = html;
        })
};

const displaySuggestedAccounts = () => {
    fetch('/api/suggestions')
        .then(response => response.json())
        .then(suggestions => {
            const html = suggestions.map(suggestions2Html).join('\n');
            document.querySelector('.suggestions').innerHTML = html;
        })
};


const initPage = () => {
    displayStories();
    displayPosts();
    displayUserProfile();
    displaySuggestedAccounts();
};



// invoke init page to display stories:
initPage();