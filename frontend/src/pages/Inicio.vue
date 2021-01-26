<template>
  <div class="q-pa-lg">
    <transition
      appear
      enter-active-class="animated fadeIn"
      leave-active-class="animated fadeOut"
    >
      <q-option-group
        v-model="linhasEscolhidas"
        :options="linhas"
        name="nome"
        color="green"
        type="checkbox"
      >

      </q-option-group>

    </transition>
    <q-btn label="Enviar" v-show="!visible" flat  class="bg-primary text-white" align="right"  @click="enviarLinhas"/>
    <q-inner-loading :showing="visible">
      <q-spinner-oval size="50px" color="primary" />
    </q-inner-loading>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'
export default {
  data: function () {
    return {
      linhasEscolhidas: [],
      visible: true
    }
  },
  created () {
    this.start()
  },
  computed: {
    ...mapState('Core', ['linhas'])
  },
  methods: {
    ...mapActions('Core', ['listarLinhas']),
    async start () {
      await this.listarLinhas()
      this.visible = false
    },
    enviarLinhas () {
      this.visible = true
      var linhas = this.linhasEscolhidas.join(',')
      this.$router.push(`/dashboard/?linhas=${linhas}`)
    }
  }
}
</script>

<style>
</style>
