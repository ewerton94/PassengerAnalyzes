<template>
    <div class="col-md-3 col-sm-12 col-xs-12">
      <q-item :style="'background-color: '+itemColor" class="q-pa-none q-ml-xs">
        <q-item-section
          side
          :style="'background-color: '+iconColor"
          class="q-pa-lg q-mr-none text-white"
        >
          <q-icon :name="iconName" color="white" size="24px"></q-icon>
        </q-item-section>
        <q-item-section class="q-pa-md q-ml-none text-white">
          <q-item-label v-if="detailComplete" class="text-white text-h6 text-weight-bolder"
            >{{ title }}
            </q-item-label
          >
          <q-item-label v-else class="text-white text-h6 text-weight-bolder"
            >

            <q-skeleton type="text" />
            </q-item-label
          >
          <q-item-label v-if="detailComplete">{{ subtitle }}</q-item-label>
          <q-item-label v-else> <q-skeleton type="text" /></q-item-label>
        </q-item-section>
      </q-item>
    </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'CardResumo',
  data: function () {
    return {
      key: 0
    }
  },
  computed: {
    ...mapState('Core', ['detailComplete'])
  },
  props: [
    'iconName',
    'iconColor',
    'itemColor',
    'title',
    'subtitle',
    'skeleton'
  ]
}
</script>

<style>
</style>
