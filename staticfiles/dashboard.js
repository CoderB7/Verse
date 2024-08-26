function format(command, value) {
    document.execCommand(command, false, value);
}

document.querySelectorAll('.editor').forEach(element => {
    element.addEventListener('focus', function () {
      if (this.innerText.trim() === this.getAttribute('data-placeholder')) {
        this.innerText = '';
        this.classList.remove('editor-placeholder');
      }
    });

    element.addEventListener('blur', function () {
      if (this.innerText.trim() === '') {
        this.innerText = this.getAttribute('data-placeholder');
        this.classList.add('editor-placeholder');
      }
    });

    element.addEventListener('input', function () {
      if (this.innerText.trim() === '') {
        this.classList.add('editor-placeholder');
      } else {
        this.classList.remove('editor-placeholder');
      }
    });
  });

  function submitPost(action) {
    const title = document.querySelector('.editor-title').innerText.trim();
    const body = document.querySelector('.editor-body').innerText.trim();
    const channelId = document.getElementById('channel-info').getAttribute('data-channel-id');

    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    const dataToSend = {
      title: title,
      body: body,
      channel_id: channelId,
    }
    console.log(action);
    let endpoint = '/dashboard/channels/' + channelId + '/post/';
    if (action === 'update') {
      const postId = document.getElementById('post-id').getAttribute('data-post-id');
      endpoint = '/dashboard/channels/' + channelId + '/post/' + postId + '/';
      dataToSend.post_id = postId;
      
    }

    fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json', 
        'X-CSRFToken': csrfToken,   // Ensure you include CSRF token for Django
      }, 
      body: JSON.stringify(dataToSend)
    })
    .then(response => {
      console.log(response.status);  // Log status codeconsole.log(response.statusText);  // Log status textreturn response.json();
      if (response.ok) {
        setTimeout(() => {
          window.location.href = '/dashboard/channels/' + channelId + '/posts/';
      }, 5000); // 5 seconds delay
      } else {
        console.error('Server responded with:', data);
        // Handle error data here
      }
    })
    .then(data => {
      
    })
    .catch((error) => {
      console.log('Endpoint:', endpoint);
      console.log('Error:', error);
      console.log('CSRF Token:', csrfToken);
      alert('Failed to fetch: ' + error.message);
    });
    
};

function submitBlogPost(action) {
  const title = document.querySelector('.editor-title').innerText.trim();
  const body = document.querySelector('.editor-body').innerText.trim();
  const blogId = document.getElementById('blog-info').getAttribute('data-blog-id');

  const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

  const dataToSend = {
    title: title,
    body: body,
    blog_id: blogId,
  }
  console.log(action);
  let endpoint = '/dashboard/blogs/' + blogId + '/post/';
  if (action === 'blog-update') {
    const postId = document.getElementById('post-id').getAttribute('data-post-id');
    endpoint = '/dashboard/blogs/' + blogId + '/post/' + postId + '/';
    dataToSend.post_id = postId;
  }
  console.log(endpoint);

  fetch(endpoint, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,  // Ensure you include CSRF token for Django
    }, 
    body: JSON.stringify(dataToSend)
  })
  .then(response => {
    if(response.ok) {
      window.location.href = '/dashboard/blogs/' + blogId + '/posts/';
    }
    else {
      return response.json().then(data => {
        window.location.href = '/dashboard/blogs/' + blogId + '/posts/';
        // Display error message to the user
      });
    }    
  })
  .catch((error) => {
    window.location.href = '/dashboard/blogs/' + blogId + '/posts/';
    alert(error);
  });
    
};   
  

