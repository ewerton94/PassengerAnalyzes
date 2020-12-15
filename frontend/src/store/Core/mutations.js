async function adaptObjectToList (list, idName, getLabelName) {
  await list.forEach((el) => {
    el.value = el[idName]
    el.label = getLabelName(el)
  })
}

const SET_LINHAS = async (state, payload) => {
  // var clientes = state.clientes
  // clientes.splice(index, index)
  // OrderSaveLocal(clientes, 'clientes', '')
  await adaptObjectToList(payload, 'numero', (el) => (el.numero + ' - ' + el.nome))
  state.linhas = payload
}
const SET_INFO_LINHAS = async (state, payload) => {
  state.linha = payload
}
const SET_INFO_GRAFICO = async (state, payload) => {
  state.graficos[payload.tipoGrafico] = {
    chartOptions: {
      chart: {
        id: 'vuechart-example'
      },
      xaxis: payload.data.xaxis
    },
    series: payload.data.series
  }
}

export {
  SET_LINHAS,
  SET_INFO_LINHAS,
  SET_INFO_GRAFICO
}
