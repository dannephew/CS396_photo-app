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
    ${renderFollowButton(suggestion)}
    `
}

const renderFollowButton = suggestion => {
    //get the user_id of the current account
    //see if that user_id is in the list of users i follow
    //if user is not currently following, then follow
    //else, unfollow

    //get list of users i follow by fetching /api/following/ 

    // const following = getListofFollowers(suggestion)
    // console.log("following: ", following)
    // console.log("suggestion: ", suggestion)
    // console.log("id: ", suggestion.id)
    // if (following.includes(suggestion)) {
    //     console.log("following does include")
    //     return `
    //     <button
    //         data-following-id="${suggestion.id}"
    //         aria-label="Follow / Unfollow"
    //         aria-checked="true"
    //         onclick="handleFollow(event);">
    //         Unfollow Me!
    //         </button>
    //     `
        //render follow button with aria-unchecked
    //suggestions are ALWAYS people you don't currently follow
    //for re-rendering, must account for switches
        return `<button
        data-following-id="${suggestion.id}"
       aria-label="Follow / Unfollow"
        aria-checked="false"
       onclick="handleFollow(event);">
           Follow Me!
       </button>`
}

const handleFollow = ev => {
    console.log("handleFollow")
    console.log("ev: ", ev)
    const elem = ev.currentTarget
    console.log("ev.currentTarget: ", elem)

    //Difference between ev and elem: 
    //ev includes the position of the mouse on the screen
    //elem is the actual button on the page that the mouse clicked
    if (elem.getAttribute('aria-checked') === 'false') {
        followSuggestion(elem)
    } else {
        unfollowSuggestion(elem)
    }
}

const followSuggestion = elem => {
    console.log("follow")
    const followId = Number(elem.dataset.followingId)
    const postData = {
        "user_id": followId
    };
    
    fetch("/api/following/", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(postData)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            redrawFollow(followId)
        });
    //fetch 
        //update the database
    //render
}

const unfollowSuggestion = elem => {
    console.log("unfollow")
    const followId = Number(elem.dataset.followingId)

    //fetch
        //update the database
    fetch(`/api/following/${followId}`, {
        method: "DELETE",
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        redrawFollow(followId)
    });
    //render
}

//////////fetch is not working. what api endpoint should i use? 
const redrawFollow = followId => {
    console.log("redraw Follow")
    //query that following object
    fetch(`/api/following/${followId}`, {
        method: "GET"
    })
        .then(response => response.json())
        .then(data => {
            console.log(data)
        })

}

// const redrawPost = postId => {
//     //requery API for post that just changed
//     fetch(`/api/posts/${postId}`)
//         .then(response => response.json())
//         .then(updatedPost => {
//             console.log(updatedPost)
//             const html = post2Html(updatedPost)
//             //redraw post
//             const newElement = stringToHTML(html)
//             const postElement = document.querySelector(`#post_${postId}`)
//             postElement.innerHTML = newElement.innerHTML
//         })
// }

const getListofFollowers = suggestion => {
    fetch('/api/following')
    .then(response => response.json())
    .then(data => {
        console.log("DATA!!!: ", data)
        return data
        //data is an array of "following" objects, with info about each person i'm following
        //Array(10)
        // 0: 
        // following: 
        // {id: 1, first_name: 'Theresa', last_name: 'Moreno', username: 'theresa_moreno', email: 'theresa_moreno@hotmail.com', …}
    })
}





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

const post2Html = post => {
    console.log("post2Html")
    return `
    <section id = "posts_${post.id}">
    <div id="post_top">
        <h2>${ post.user.username} - ${post.current_user_like_id} - ${post.current_user_bookmark_id}</h2>
        <h4>•••</h4>
    </div>
    <img src=${ post.image_url} id="post_pic" alt="post image of ${post.user.username}"/>
    <section class="post_bottom">
            <div id = "post_icons">
                <div>
                    ${  renderLikeButton(post)  }
                    ${  renderBookmarkButton(post)  }
                    <i class="far fa-comment"></i>
                    <i class="far fa-paper-plane"></i>
                </div>
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
// const modalElement = document.querySelector('.modal-bg');

// const openModal = ev => {
//     console.log("open!")
// }

// const closeModal = ev => {
//     console.log("close!")
// }

const getCommentButton = (post) => {
    if (post.comments.length > 1) {
        return `
        <button>View all ${post.comments.length} Comments</button>
        `
    } else if (post.comments.length == 1){
        return `
        <p>${ post.comments[0].text }</p>
        `
    } else {
        return ``
    }

}

// const toggleLike = (postid, like_id) => {
//     //has this already been liked
//     if (like_id == null){
//         console.log(postid)
//         const url = `/api/posts/${postid}/likes/` 
//         console.log(url)

//         fetch(url, {method: 'POST'})
//         //tell server we're using post request, not get request
//         .then(response => response.json())
//         .then(like => {
//             console.log(like)

//             //requery server for POST
//             /////redraw the post -- do we need to do this without reloading page?
//             //document.querySelector
//         })}
//     else{
//         console.log("You've already liked this. Delete like")
//         const url = `/api/posts/${postid}/likes/${like_id}` 
//         fetch(url, {method: 'DELETE'})
//         //tell server we're using post request, not get request
//         .then(response => response.json())
//         .then(like => {
//             console.log(like)
//             /////redraw the post -- do we need to do this without reloading page?
            
//         })
//     }
// }
// Issue post request
// Then it responds, but post object is not in sync
// Actually has more likes
//Must requery and get fresh copy of post object
//invoke post2html

const renderLikeButton = post => {
    if (post.current_user_like_id) {
        return `
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
}

const handleBookmark = ev => {
    console.log("Handle bookmark functionality")
    const elem = ev.currentTarget
    //^retrieves the attributes of the button 
    if (elem.getAttribute('aria-checked') === 'true') {
        console.log('unbookmark post')
       unbookmarkPost(elem)
    } else {
        console.log('bookmark post')
        bookmarkPost(elem)
    }
}

const unbookmarkPost = elem => {
    const postId = Number(elem.dataset.postId)
    console.log("unbookmark post", elem)
    //data-like-id can only be retrieved in camel case
    /////fetch is different in API docs -- also needs the post id
    fetch(`/api/bookmarks/${elem.dataset.bookmarkId}`, {
        method: "DELETE",
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log("redraw post", data)
        //redraw post
        redrawPost(postId)
    })
    
}

const bookmarkPost = elem => {
    const postId = Number(elem.dataset.postId)
    console.log("bookmark post", elem)

    const postData = {
        "post_id": postId
    };
    fetch(`/api/bookmarks/`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(postData)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        console.log("redraw post", data)
        redrawPost(postId)
    });

}


const handleLike = ev => {
    console.log("Handle like functionality")
    // if area-checked == 'true' then Delete Like Object
    //else: Issue a POST request to create a Like Object
    const elem = ev.currentTarget
        //^retrieves the attributes of the button 
    if (elem.getAttribute('aria-checked') === 'true') {
        console.log('unlike post')
        unlikePost(elem)
    } else {
        console.log('like post')
        likePost(elem)
    }
}

const unlikePost = elem => {
    const postId = Number(elem.dataset.postId)
    console.log("unlike post", elem)
    //data-like-id can only be retrieved in camel case
    //fetch is different in API docs -- also needs the post id
    fetch(`/api/posts/${elem.dataset.postId}/likes/${elem.dataset.likeId}`, {
        method: "DELETE",
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log("redraw post", data)
        //redraw post
        redrawPost(postId)
    })
    
}

const likePost = elem => {
    const postId = Number(elem.dataset.postId)
    console.log("like post", elem)

    const postData = {};
    fetch(`/api/posts/${elem.dataset.postId}/likes/`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(postData)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        console.log("redraw post", data)
        redrawPost(postId)
    });

}

const stringToHTML = htmlString => {
    var parser = new DOMParser()
    var doc = parser.parseFromString(str, 'text/html')
    return doc.body.firstChild
}

///////////not working
const redrawPost = postId => {
    //requery API for post that just changed
    fetch(`/api/posts/${postId}`)
        .then(response => response.json())
        .then(updatedPost => {
            console.log(updatedPost)
            const html = post2Html(updatedPost)
            //redraw post
            const newElement = stringToHTML(html)
            const postElement = document.querySelector(`#post_${postId}`)
            postElement.innerHTML = newElement.innerHTML
        })
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