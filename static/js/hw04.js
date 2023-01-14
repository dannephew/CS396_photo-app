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
                    <h4 id="post_words" class="name">${ post.likes} likes</h4>
                </div>
                <div class="post_descrip_div">
                    <h5 class = "name" id="post_words">{{ c.get('user').get('username') }}</h5>
                    <h5 id="post_words"> {{ c.get('title') }} </h5>
                </div>
                
                {% if c.get('comments')|length > 1 %}
                    <h5 id="post_words"><a href="more">View all {{c.get('comments')|length}} comments</a></h5>
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
        <h2>${ post.user.username}</h2>
        <h4>•••</h4>
    </div>
    <img src=${ post.image_url} id="post_pic" alt="post image of ${post.user.username}"/>
    <section class="post_bottom">
            <div id = "post_icons">
                <div>
                    <i class="far fa-heart"></i>
                    <i class="far fa-comment"></i>
                    <i class="far fa-paper-plane"></i>
                </div>
                <i class="far fa-bookmark"></i>
            </div>
        <div>
            <p>${ post.caption }</p>
        </div>
        </section>
    </section>
    `;
};

const displayPosts = () => {
    console.log("displayPosts")
    fetch('/api/posts')
        .then(response => response.json())
        .then(posts => {
            const html = posts.map(post2Html).join('\n');
            document.querySelector('#posts').innerHTML = html;
        })
};

const initPage = () => {
    displayStories();
    displayPosts();
};

// invoke init page to display stories:
initPage();