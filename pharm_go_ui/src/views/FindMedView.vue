<template>
  <div class="findMed">
    <h1>This is an about page</h1>
    <input v-model="query">
    <button @click="getMeds">Find Med</button>
    <br>
    <div>
      <pre>{{ med }}</pre>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  setup() {
    let query = ""
    let med = []

    function getMeds() {
      // .value is needed in JavaScript
      console.log(`GET MEDS: ${this.query}`)
      // const axios = require('axios');
      axios({
        method: 'get',
        url: `http://192.168.10.104:5005/med/${this.query}`,
      }).then(
          ({data}) => {
            console.log(data)
            this.med = data
          }
      )

    }

    // don't forget to expose the function as well.
    return {
      med,
      query,
      getMeds
    }
  }
}

</script>

<style>
@media (min-width: 1024px) {
  .findMed {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
