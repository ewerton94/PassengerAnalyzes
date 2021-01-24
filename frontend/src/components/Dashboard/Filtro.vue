<template>
  <div class="q-ma-md">
    <q-expansion-item expand-separator icon="fas fa-filter" label="Filtro" >
      <div class="row justify-between q-my-md">
        <div class="col-12 col-md-3 q-pa-sm">
          <div class="row">

        <q-btn-dropdown color="primary" class="col-12 col-md-12">
        <template v-slot:label>
          <div class="row items-center no-wrap">
            <q-icon left class="float-left" name="calendar_today" avatar />
            <q-separator></q-separator>
            <div class="text-center">
              Dias de análise<br /><small>Filtro por data</small>
            </div>
          </div>
        </template>
        <div class="col-12 q-ma-md">
          <q-input
            class="col-12 q-mt-md"
            filled
            label="Data inicial"
            v-model="filtrarDataInicial"
            mask="date"
          >
            <template v-slot:append>
              <q-icon name="event" class="cursor-pointer">
                <q-popup-proxy
                  ref="qDateProxy"
                  transition-show="scale"
                  transition-hide="scale"
                >
                  <q-date
                    v-model="filtrarDataInicial"
                    @input="() => $refs.qDateProxy.hide()"
                  />
                </q-popup-proxy>
              </q-icon>
            </template>
          </q-input>
          <q-separator />
          <q-input
            class="col-12 q-mt-md"
            filled
            label="Data final"
            v-model="filtrarDataFinal"
            mask="date"
          >
            <template v-slot:append>
              <q-icon name="event" class="cursor-pointer">
                <q-popup-proxy
                  ref="qDateProxy"
                  transition-show="scale"
                  transition-hide="scale"
                >
                  <q-date
                    v-model="filtrarDataFinal"
                    @input="() => $refs.qDateProxy.hide()"
                  />
                </q-popup-proxy>
              </q-icon>
            </template>
          </q-input>
        </div>
      </q-btn-dropdown>
      </div>
        </div>

      <div class="col-12 col-md-3 q-pa-sm">
        <div class="row">
      <q-btn-dropdown color="primary" class="col-12 col-md-12">
        <template v-slot:label>
          <div class="row items-center no-wrap">
            <q-icon left name="calendar_today" />
            <div class="text-center">
              Dia da semana<br /><small>Filtro por dia</small>
            </div>
          </div>
        </template>
        <div class="col-12 q-ma-md">
          <div class="row">
          <q-checkbox class="col-12" v-model="filtrarDiasDaSemana" :val="1" label="Domingo" />
          </div>
          <div class="row">
          <q-checkbox class="col-12" v-model="filtrarDiasDaSemana" :val="2" label="Segunda-Feira" />
          </div>
          <div class="row">
          <q-checkbox class="col-12" v-model="filtrarDiasDaSemana" :val="3" label="Terça-Feira" />
          </div>
          <div class="row">
          <q-checkbox class="col-12" v-model="filtrarDiasDaSemana" :val="4" label="Quarta-Feira" />
          </div>
          <div class="row">
          <q-checkbox class="col-12" v-model="filtrarDiasDaSemana" :val="5" label="Quinta-Feira" />
          </div>
          <div class="row">
          <q-checkbox class="col-12" v-model="filtrarDiasDaSemana" :val="6" label="Sexta-Feira" />
          </div>
          <div class="row">
          <q-checkbox class="col-12" v-model="filtrarDiasDaSemana" :val="7" label="Sábado" />
          </div>

        </div>
      </q-btn-dropdown>
      </div>
        </div>
      <div class="col-12 col-md-3 q-pa-sm">
        <div class="row">
      <q-btn-dropdown color="primary" class="col-12 col-md-12">
        <template v-slot:label>
          <div class="row items-center no-wrap">
            <q-icon left name="timer" />
            <div class="text-center">
              Faixa Horária de Embarque<br /><small>Filtro por hora</small>
            </div>
          </div>
        </template>
        <div class="col-12 q-ma-md">
          <q-input
            class="col-12 q-mt-md"
            filled
            label="Hora inicial"
            v-model="filtrarHoraInicialEmbarque"
            mask="time"
          >
            <template v-slot:append>
              <q-icon name="timer" class="cursor-pointer">
                <q-popup-proxy
                  ref="qDateProxy"
                  transition-show="scale"
                  transition-hide="scale"
                >
                  <q-time
                    v-model="filtrarHoraInicialEmbarque"
                    @input="() => $refs.qDateProxy.hide()"
                  />
                </q-popup-proxy>
              </q-icon>
            </template>
          </q-input>
          <q-separator />
          <q-input
            class="col-12 q-mt-md"
            filled
            label="Hora final"
            v-model="filtrarHoraFinalEmbarque"
            mask="time"
          >
            <template v-slot:append>
              <q-icon name="timer" class="cursor-pointer">
                <q-popup-proxy
                  ref="qDateProxy"
                  transition-show="scale"
                  transition-hide="scale"
                >
                  <q-time
                    v-model="filtrarHoraFinalEmbarque"
                    @input="() => $refs.qDateProxy.hide()"
                  />
                </q-popup-proxy>
              </q-icon>
            </template>
          </q-input>
        </div>
      </q-btn-dropdown>
      </div>
        </div>
      <div class="col-12 col-md-3 q-pa-sm">
        <div class="row">
      <q-btn-dropdown color="primary" class="col-12 col-md-12">
        <template v-slot:label>
          <div class="row items-center no-wrap">
            <q-icon left name="fas fa-map-signs" />
            <div class="text-center">
              Sentido de viagem<br /><small>Filtro por sentido</small>
            </div>
          </div>
        </template>
        <div class="col-12 q-ma-md">
          <q-select
            class="col-12"
            outlined
            v-model="filtrarSentido"
            :options="['IDA', 'VOLTA', 'AMBOS']"
          >
            <template v-slot:prepend>
              <q-icon name="fas fa-map-signs" />
            </template>
          </q-select>
        </div>
      </q-btn-dropdown>
      </div>
        </div>

      </div>

      <div class="row justify-end">
        <q-btn
          label="Filtrar"
          align="right"
          flat
          color="white"
          class="bg-primary"
          @click="filtrarDados"
          :disable="!detailComplete"
        />
      </div>

    </q-expansion-item>
  </div>
</template>

<script>
import { mapMutations, mapActions, mapState } from 'vuex'
export default {
  name: 'EssentialLink',
  data: function () {
    return {
      filtrarDataInicial: null,
      filtrarDataFinal: null,
      filtrarDiasDaSemana: [],
      filtrarHoraInicialEmbarque: null,
      filtrarHoraFinalPartida: null,
      filtrarHoraFinalEmbarque: null,
      filtrarSentido: 'AMBOS'
    }
  },
  computed: {
    ...mapState('Core', ['extraFiltro', 'detailComplete'])
  },
  methods: {
    ...mapMutations('Core', [
      'ADD_NEW_EXTRA_FILTRO',
      'ICREMENT_GERALKEY',
      'SET_ENDED'
    ]),
    ...mapActions('Core', ['detalharLinhas']),
    async filtrarDados () {
      await this.SET_ENDED(false)
      if (this.filtrarDataInicial && this.filtrarDataFinal) {
        await this.ADD_NEW_EXTRA_FILTRO({
          newExtraFiltroKey: 'data_inicial',
          newExtraFiltroValue: this.filtrarDataInicial.replaceAll('/', '-')
        })
        await this.ADD_NEW_EXTRA_FILTRO({
          newExtraFiltroKey: 'data_final',
          newExtraFiltroValue: this.filtrarDataFinal.replaceAll('/', '-')
        })
      }
      if (this.filtrarDiasDaSemana.length) {
        await this.ADD_NEW_EXTRA_FILTRO({
          newExtraFiltroKey: 'dias_da_semana',
          newExtraFiltroValue: this.filtrarDiasDaSemana.join(',')
        })
      }
      if (this.filtrarHoraInicialEmbarque && this.filtrarHoraFinalEmbarque) {
        await this.ADD_NEW_EXTRA_FILTRO({
          newExtraFiltroKey: 'embarque_inicial',
          newExtraFiltroValue: this.filtrarHoraInicialEmbarque
        })
        await this.ADD_NEW_EXTRA_FILTRO({
          newExtraFiltroKey: 'embarque_final',
          newExtraFiltroValue: this.filtrarHoraFinalEmbarque
        })
      }
      if (this.filtrarSentido) {
        await this.ADD_NEW_EXTRA_FILTRO({
          newExtraFiltroKey: 'sentido',
          newExtraFiltroValue: this.filtrarSentido
        })
      }

      this.ICREMENT_GERALKEY()
      await this.detalharLinhas(this.extraFiltro)
    }
  },
  props: {}
}
</script>
