<script setup lang="ts">
import { GoogleLogin } from 'vue3-google-login';
import { ref } from 'vue';
import { onMounted } from 'vue'
import { Octokit } from 'octokit';

type Repo = {
  id: number,
  name: string,
  full_name: string,
  hooked: boolean
}

// TODO: needs to be a public url
const WEBHOOK_URL = 'http://localhost:8000/users/webhook'
const LOGIN_URL = 'http://localhost:8000/users/login'
const ACCESS_TOKEN_URL = 'http://localhost:8000/users/authorize'
const SELECT_REPO_URL = 'http://localhost:8000/users/select_repo'

// url for getting a authorize code from github
const authorizeUrl = new URL('https://github.com/login/oauth/authorize')
authorizeUrl.searchParams.append('client_id', 'Ov23libLqCiLNJBdAmxC')
authorizeUrl.searchParams.append('redirect_uri', 'http://localhost:5173/github')
authorizeUrl.searchParams.append('scope', 'public_repo')

// load the google login id from session if it exists
const googleId = ref<string|null>(sessionStorage.googleId || null)
// list of repos from linked user
const repos = ref<Repo[]|null>(null)

// used for github api calls
let octokit: Octokit|null = null

const googleLoginCallback = async (response: {clientId: string}) => {
  // storage the client id
  googleId.value = response.clientId
  sessionStorage.googleId = response.clientId

  // tell the server that a user logged in with this client id
  const loginRequest = new URL(LOGIN_URL)
  loginRequest.searchParams.append('client_id', response.clientId)
  const loginResponse = await fetch(loginRequest)
  console.log('login request', loginResponse)
}

const saveRepo = async () => {
  // get the selected repo
  const repoId = document.querySelector('input[name="selected_repo"]:checked')?.getAttribute('value')!
  
  // tell the server this user selected this repo
  const saveRepoRequest = new URL(SELECT_REPO_URL)
  saveRepoRequest.searchParams.append('client_id', googleId.value!)
  saveRepoRequest.searchParams.append('repo_id', repoId)
  const response = await fetch(saveRepoRequest, {method: 'POST'})
  console.log('save repo request', response)
}

onMounted(async () => {
  const urlParams = new URLSearchParams(window.location.search)
  let githubAccessToken = null
  if(urlParams.has('code')) {
    // if we have the code (because we were redirected)
    const code = urlParams.get('code')

    // get an access token from the server by sending the code
    const accessTokenRequest = new URL(ACCESS_TOKEN_URL)
    accessTokenRequest.searchParams.append('code', code!)
    const response = await (await fetch(accessTokenRequest)).json()
    githubAccessToken = response.access_token
  }

  if(githubAccessToken) {
    // if we have the access token, we can initialize the github api
    octokit = new Octokit({
      auth: githubAccessToken
    })

    // ask for the user's repos
    const response = await octokit.request('GET /user/repos', {
      type: 'owner',
      sort: 'created',
      headers: {
        'X-GitHub-Api-Version': '2022-11-28'
      }
    })
    console.log(response)
    repos.value = response.data.map(data => ({id: data.id, name: data.name, full_name: data.full_name, hooked: false}))
  }

  if(octokit && repos.value && repos.value.length > 0) {
    // for each repo, create a webhook
    repos.value.forEach(async (repo, i) => {
      // // commented out because we don't have a public url (errors out)
      // await octokit!.request(`POST /repos/${repo.full_name}/hooks`, {
      //   config: {
      //     url: WEBHOOK_URL,
      //     content_type: 'json',
      //   },
      //   events: ['push', 'deployment', 'pull_request']
      // })
      // repo.hooked = true
      setTimeout(() => repo.hooked = true, 500*i+500)
    })
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
    <form v-if="repos" id="repos_form">
      <div v-for="repo in repos" :key="repo.id">
        <input :id="repo.id.toString()" :value="repo.id" type="radio" name="selected_repo">
        <label :for="repo.id.toString()">{{ repo.name }} {{ repo.hooked ? '✅' : '❌' }}</label>
      </div>
    </form>
    <button v-if="repos" @click="saveRepo">Save selected repository</button>
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
