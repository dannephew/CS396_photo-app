const story2Html = story => {
    return `
        <div>
            <img src="${ story.user.thumb_url }" class="pic" alt="profile pic for ${ story.user.username }" />
            <p>${ story.user.username }</p>
        </div>
    `;
};

// fetch data from your API endpoint:
const displayStories = () => {
    fetch('/api/stories') 
        .then(response => response.json()) //promise: 
        //usually time is predictable
        //api call not in your hands; must request data and data needs to be returned. time is unknown
        //certain statement should only be executed after previous statement is executed
        .then(stories => {
            const html = stories.map(story2Html).join('\n');
            document.querySelector('.stories').innerHTML = html;
        }) //generate into html element
};

/*
{% for post in posts %}



            <div class="comments">
                {% if post.get('comments')|length > 1 %}
                    <p><button class="link">View all {{ post.get('comments')|length }} comments</button></p>
                {% endif %}
                {% for comment in post.get('comments')[:1] %}
                    <p>
                        <strong>{{ comment.get('user').get('username') }}</strong> 
                        {{ comment.get('text') }}
                    </p>
                {% endfor %}
                <p class="timestamp">{{ post.get('display_time') }}</p>
            </div>
        </div>
        <div class="add-comment">
            <div class="input-holder">
                <input type="text" aria-label="Add a comment" placeholder="Add a comment...">
            </div>
            <button class="link">Post</button>
        </div>
    </section>
*/

const destroyModal = ev => {
    document.querySelector('#modal-container').innerHTML = ""
}

const showPostDetail = ev => {
    const postId = ev.currentTarget.dataset.postId
    fetch(`/api/posts/${postId}`)
        .then(response => response.json())
        .then(post => {
            const html = `
            <div class="modal-bg">
                <button onclick="destroyModal(event)">Close</button>
                <div class = "modal">
                    <img src="${post.image_url}"/>
                </div>
            </div>
            `
            document.querySelector('#modal-container').innerHTML = html
        })

    
}

const displayComments = (comments, postID) => {
    let html = ''
    if (comments.length > 1) {
        html += `
            <button class="link" data-post-id="${postID}" onclick="showPostDetail(event)">view all ${comments.length} comments</button>
        `
    }
    if (comments && comments.length > 0) {
        const lastComment = comments[comments.length - 1]
        html += `
        <p>
            <strong>${lastComment.user.username}</strong>
            ${lastComment.text}
            <div>${lastComment.display_time}</div>
        </p>
        `
    }
    html += `
    <div class="add-comment">
        <div class="input-holder">
            <input type="text" aria-label="Add a comment" placeholder="Add a comment...">
        </div>
        <button class="link">Post</button>
    </div>
    `
    return `<div class="comments">${html}</div>`
}

const likeUnlike = ev => {
    console.log('like/unlike button clicked');
}

const post2Html = post => {
    return `
        <section class="card">
            <div class="header">
                <h3>${ post.user.username } </h3>
                <i class="fa fa-dots"></i>
            </div>
            <img src="${ post.image_url }" alt="Image posted by ${ post.user.username }" width="300" height="300">
            <div class="info">
                <div class="buttons">
                    <div>
                        <button onclick="likeUnlike(event)">
                            <i class="fa${post.current_user_like_id ? 's' : 'r'} fa-heart"></i>
                        </button>
                            <i class="far fa-comment"></i>
                            <i class="far fa-paper-plane"></i>
                    </div>
                    <div>
                        <i class="fa${post.current_user_bookmark_id ? 's' : 'r'} fa-bookmark"></i>
                    </div>
                </div>
            </div>
            <p class="likes"><strong>${ post.likes.length } like${post.likes.length != 1 ? 's' : ''} </strong></p>
            <div class="caption">
                <p>
                    <strong>${ post.user.username }</strong> 
                    ${ post.caption } 
                </p>
            </div>
            ${ displayComments(post.comments, post.id) }
        </div>


        </section>
    `;
};

// fetch data from your API endpoint:
const displayPosts = () => {
    fetch('/api/posts') 
        .then(response => response.json()) //promise: 
        //usually time is predictable
        //api call not in your hands; must request data and data needs to be returned. time is unknown
        //certain statement should only be executed after previous statement is executed
        .then(posts => {
            const html = posts.map(post2Html).join('\n');
            document.querySelector('#posts').innerHTML = html;
        }) //generate into html element
};

//get post data from API endpoint (/api/posts?limit=10)
//when data arrives, build a bunch of HTML cards (ie a big string)
//update the container and put HTML on the inside of it 

const initPage = () => {
    displayStories();
    displayPosts();
};

// invoke init page to display stories:
initPage();