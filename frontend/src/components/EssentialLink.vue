<template>
  <q-list bordered class="rounded-borders">
    <q-expansion-item
      expand-separator
      icon="calendar_today"
      label="Dias de análise"
      caption="Filtro por Data"
    >
      <q-card>
        <q-card-section>
          <q-toolbar>
            <q-toolbar-title style="font-weight: bold color"
              >Intervalo de tempo</q-toolbar-title
            >
          </q-toolbar>
          <div class="row">
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
        </q-card-section>
      </q-card>
    </q-expansion-item>
    <q-expansion-item
      expand-separator
      icon="timer"
      label="Faixa Horária de Partida"
      caption="Filtro por hora"
    >
      <q-card>
        <q-card-section>
          <q-toolbar>
            <q-toolbar-title style="font-weight: bold color"
              >Intervalo de tempo</q-toolbar-title
            >
          </q-toolbar>
          <div class="row">
            <q-input
              class="col-12 q-mt-md"
              filled
              label="Hora inicial"
              v-model="filtrarHoraInicialPartida"
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
                      v-model="filtrarHoraInicialPartida"
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
              v-model="filtrarHoraFinalPartida"
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
                      v-model="filtrarHoraFinalPartida"
                      @input="() => $refs.qDateProxy.hide()"
                    />
                  </q-popup-proxy>
                </q-icon>
              </template>
            </q-input>
          </div>
        </q-card-section>
      </q-card>
    </q-expansion-item>
    <q-expansion-item
      expand-separator
      icon="timer"
      label="Faixa Horária de Embarque"
      caption="Filtro por hora"
    >
      <q-card>
        <q-card-section>
          <q-toolbar>
            <q-toolbar-title style="font-weight: bold color"
              >Intervalo de tempo</q-toolbar-title
            >
          </q-toolbar>
          <div class="row">
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
        </q-card-section>
      </q-card>
    </q-expansion-item>
    <q-btn label="Filtrar" align="right" flat color="primary" @click="filtrarDados"/>
  </q-list>
</template>

<script>
import { mapMutations, mapActions, mapState } from 'vuex'
export default {
  name: 'EssentialLink',
  data: function () {
    return {
      filtrarDataInicial: null,
      filtrarDataFinal: null,
      filtrarHoraInicialPartida: null,
      filtrarHoraInicialEmbarque: null,
      filtrarHoraFinalPartida: null,
      filtrarHoraFinalEmbarque: null
    }
  },
  computed: {
    ...mapState('Core', ['extraFiltro'])

  },
  methods: {
    ...mapMutations('Core', ['ADD_NEW_EXTRA_FILTRO', 'ICREMENT_GERALKEY', 'SET_ENDED']),
    ...mapActions('Core', ['detalharLinhas']),
    async filtrarDados () {
      await this.SET_ENDED(false)
      if (this.filtrarDataInicial && this.filtrarDataFinal) {
        await this.ADD_NEW_EXTRA_FILTRO({ newExtraFiltroKey: 'data_inicial', newExtraFiltroValue: this.filtrarDataInicial.replaceAll('/', '-') })
        await this.ADD_NEW_EXTRA_FILTRO({ newExtraFiltroKey: 'data_final', newExtraFiltroValue: this.filtrarDataFinal.replaceAll('/', '-') })
      }
      if (this.filtrarHoraInicialPartida && this.filtrarHoraFinalPartida) {
        await this.ADD_NEW_EXTRA_FILTRO({ newExtraFiltroKey: 'partida_inicial', newExtraFiltroValue: this.filtrarHoraInicialPartida })
        await this.ADD_NEW_EXTRA_FILTRO({ newExtraFiltroKey: 'partida_final', newExtraFiltroValue: this.filtrarHoraFinalPartida })
      }
      if (this.filtrarHoraInicialEmbarque && this.filtrarHoraFinalEmbarque) {
        await this.ADD_NEW_EXTRA_FILTRO({ newExtraFiltroKey: 'embarque_inicial', newExtraFiltroValue: this.filtrarHoraInicialEmbarque })
        await this.ADD_NEW_EXTRA_FILTRO({ newExtraFiltroKey: 'embarque_final', newExtraFiltroValue: this.filtrarHoraFinalEmbarque })
      }

      this.ICREMENT_GERALKEY()
      await this.detalharLinhas(this.extraFiltro)
    }

  },
  props: {

  }
}
</script>
