import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import vue3GoogleLogin from 'vue3-google-login'
import { createOAuthClient, SessionStorage } from '@volverjs/auth-vue'

const githubAuthClient = createOAuthClient({
  url: 'https://github.com/login/oauth/authorize',
  clientId: 'Ov23libLqCiLNJBdAmxC',
  storage: new SessionStorage('github-login'),
  redirectUri: 'http://localhost:5173/github',
  postLogoutRedirectUri: 'http://localhost:5173/github'
})
githubAuthClient.initialize()

const app = createApp(App)

app.use(vue3GoogleLogin, {
  'clientId': '110368998033-2qoprelajj6qice7l5rfedqgch8tr1ug.apps.googleusercontent.com'
})
app.use(githubAuthClient, {
  global: true
})
app.use(router)

app.mount('#app')
