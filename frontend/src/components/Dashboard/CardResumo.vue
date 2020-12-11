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
          <q-item-label class="text-white text-h6 text-weight-bolder"
            >{{ title }}</q-item-label
          >
          <q-item-label>{{ subtitle }}</q-item-label>
        </q-item-section>
      </q-item>
    </div>
</template>

<script>

export default {
  name: 'CardResumo',
  data: function () {
    return {
      key: 0
    }
  },
  props: [
    'iconName',
    'iconColor',
    'itemColor',
    'title',
    'subtitle'
  ]
}
</script>

<style>
</style>
