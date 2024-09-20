<script setup lang="ts">
import { GoogleLogin } from 'vue3-google-login';
import { ref } from 'vue';
import { onMounted } from 'vue'
import { Octokit } from 'octokit';

type Repo = {
  id: number,
  name: string
}

const googleId = ref(null)
const repos = ref<Repo[]>([])

const googleLoginCallback = (response) => {
  googleId.value = response.clientId
}

const authorizeUrl = new URL('https://github.com/login/oauth/authorize')
authorizeUrl.searchParams.append('client_id', 'Ov23libLqCiLNJBdAmxC')
authorizeUrl.searchParams.append('redirect_uri', 'http://localhost:5173/github')
authorizeUrl.searchParams.append('scope', 'public_repo')

onMounted(async () => {
  const urlParams = new URLSearchParams(window.location.search)
  let githubAccessToken = null
  if(urlParams.has('code')) {
    const code = urlParams.get('code')

    const accessTokenRequest = new URL('http://localhost:8000/authorize')
    accessTokenRequest.searchParams.append('code', code!)
    const response = await (await fetch(accessTokenRequest)).json()
    githubAccessToken = response.access_token
  }

  if(githubAccessToken) {
    const octokit = new Octokit({
      auth: githubAccessToken
    })
    const response = await octokit.request('GET /user/repos', {
      headers: {
        'X-GitHub-Api-Version': '2022-11-28'
      }
    })
    console.log(response)
    repos.value = response.data
  }
  
})


</script>

<template>
  <div class="about">
    <h1>This is an about page</h1>
    <div>
      <GoogleLogin :callback="googleLoginCallback"/>
      <a v-if="googleId" :href="authorizeUrl.toString()">Link Github</a>
    </div>
    <select v-if="repos">
      <option v-for="repo in repos" :key="repo.id" :value="repo.id">
        {{ repo.name }}
      </option>
    </select>
  </div>
</template>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
  }
}
</style>
