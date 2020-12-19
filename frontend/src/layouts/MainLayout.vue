<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="leftDrawerOpen = !leftDrawerOpen"
        />

        <q-toolbar-title>
          Análises de Passageiros
        </q-toolbar-title>

        <div>Quasar v{{ $q.version }}</div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      content-class="bg-grey-1"
    >
      <q-list>
        <q-item-label
          header
          class="text-grey-8"
        >
          Menu
        </q-item-label>
        <q-list>
        <q-item clickable v-close-popup href="/">
          <q-item-section avatar>
          <q-icon color="primary" name="dashboard" />
        </q-item-section>
          <q-item-section>
            <q-item-label>Dashboard</q-item-label>
          </q-item-section>
        </q-item>

        <q-item clickable v-close-popup @click="calcularDesembarque">
          <q-item-section avatar>
          <q-icon color="primary" name="fas fa-calculator" />
        </q-item-section>
          <q-item-section>
            <q-item-label>Calcular Desembarques</q-item-label>
          </q-item-section>
        </q-item>

      </q-list>

      </q-list>
    </q-drawer>

    <q-page-container >
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'MainLayout',
  methods: {
    ...mapActions('Core', ['calcularDesembarque'])
  },

  data () {
    return {
      leftDrawerOpen: false
    }
  }
}
</script>
