import { HTTPClient } from 'boot/axios'
import { handleError } from 'boot/exceptions'
// import { Notify } from 'quasar'
function serialize (obj) {
  var str = []
  for (var p in obj) { str.push(encodeURIComponent(p) + '=' + encodeURIComponent(obj[p])) }
  return str.join('&')
}
const listarLinhas = ({ commit }) => {
  return new Promise((resolve, reject) => {
    HTTPClient.get('core/linhas/')
      .then(async (suc) => {
        console.log(suc.data)
        await commit('SET_LINHAS', suc.data)
        resolve(suc.data)
      })
      .catch(async (err) => {
        err = await err
        handleError(err)
        reject(err)
      })
  })
}

const detalharLinhas = ({ commit }, extraFiltro) => {
  return new Promise((resolve, reject) => {
    HTTPClient.get(`core/linhas/detalhar/?${serialize(extraFiltro)}`)
      .then(async (suc) => {
        console.log(suc.data)
        await commit('SET_INFO_LINHAS', suc.data)
        resolve(suc.data)
      })
      .catch(async (err) => {
        err = await err
        handleError(err)
        reject(err)
      })
  })
}
const obterDadosGrafico = ({ commit }, extraFiltro) => {
  return new Promise((resolve, reject) => {
    HTTPClient.get(`core/linhas/grafico/?${serialize(extraFiltro)}`)
      .then(async (suc) => {
        // console.log(suc.data)
        await commit('SET_INFO_GRAFICO', { data: suc.data, tipoGrafico: extraFiltro.tipo_grafico })
        resolve(suc.data)
      })
      .catch(async (err) => {
        err = await err
        handleError(err)
        reject(err)
      })
  })
}

export {
  listarLinhas,
  detalharLinhas,
  obterDadosGrafico

}
