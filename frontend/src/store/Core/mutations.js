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
const SET_INFO_LINHAS = (state, payload) => {
  state.linha = payload
  state.detailComplete = true
}
const SET_INFO_GRAFICO = (state, payload) => {
  state.graficos[payload.tipoGrafico] = payload.data
  /// console.log(state.graficos[payload.tipoGrafico])
}

const ICREMENT_GERALKEY = (state, payload) => {
  state.geralKey = state.geralKey + 1
}
const SET_ENDED = (state, payload) => {
  state.detailComplete = payload
}
const SET_EXTRA_FILTRO = (state, extraFiltro) => {
  state.extraFiltro = extraFiltro
  ICREMENT_GERALKEY(state, extraFiltro)
}
const CLEAN_EXTRA_FILTRO = (state) => {
  state.extraFiltro = {}
}

const ADD_NEW_EXTRA_FILTRO = (state, { newExtraFiltroKey, newExtraFiltroValue }) => {
  state.extraFiltro[newExtraFiltroKey] = newExtraFiltroValue
  ICREMENT_GERALKEY(state, newExtraFiltroKey)
}
const ADD_EXTRA_FILTRO_INICIAL = (state, { newExtraFiltroKey, newExtraFiltroValue }) => {
  state.extraFiltro[newExtraFiltroKey] = newExtraFiltroValue
  // ICREMENT_GERALKEY(state, newExtraFiltroKey)
}

export {
  SET_LINHAS,
  SET_INFO_LINHAS,
  SET_INFO_GRAFICO,
  ICREMENT_GERALKEY,
  SET_EXTRA_FILTRO,
  SET_ENDED,
  ADD_NEW_EXTRA_FILTRO,
  ADD_EXTRA_FILTRO_INICIAL,
  CLEAN_EXTRA_FILTRO
}
