<template>
  <div class="hello">
    <h1>Login</h1>
    <p>Token: {{ $store.state.token }}</p>
    <p>Error: {{ error }}</p>
    <mu-text-field label='Email' labelFloat v-model='email'/></br>
    <mu-text-field label='Password' type='password' labelFloat v-model='password'/></br>
    <mu-raised-button label='Login' class='demo-raised-button' primary @click='login'/>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'login',
  computed: mapGetters[{ token: 'token' }],
  data () {
    return {
      email: '',
      password: '',
      error: null
    }
  },
  methods: {
    async login () {
      try {
        await this.$store.dispatch('login', {
          email: this.email,
          password: this.password
        })
        this.email = ''
        this.password = ''
        this.error = null
      } catch (e) {
        this.error = e.message
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #35495E;
}
</style>
