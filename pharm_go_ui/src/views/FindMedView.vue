<template>
  <div class="findMed">
    <h1>This is an about page</h1>
    <input v-model="query">
    <button @click="getMeds">Find Med</button>
    <br>
    <div v-if="med">
      <h2>Fetched Data:</h2>
      <pre>{{ med }}</pre>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  setup() {
    let query = ""
    let med = undefined

    async function getMeds() {
      // .value is needed in JavaScript
      console.log(`GET MEDS: ${this.query}`)
      // const axios = require('axios');

      const response = await axios.get(`http://192.168.10.104:5005/med/${this.query}`);
      this.med = response.data
      console.log(this.med)
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
