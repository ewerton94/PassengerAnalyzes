import { HTTPClient } from 'boot/axios'
import { handleError } from 'boot/exceptions'
// import { Notify } from 'quasar'

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

const detalharLinhas = ({ commit }, linhas) => {
  return new Promise((resolve, reject) => {
    HTTPClient.get(`core/linhas/detalhar/?linhas=${linhas}`)
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
const obterDadosGrafico = ({ commit }, { linhas, tipoGrafico }) => {
  return new Promise((resolve, reject) => {
    HTTPClient.get(`core/linhas/grafico/?tipo_grafico=${tipoGrafico}&linhas=${linhas}`)
      .then(async (suc) => {
        console.log(suc.data)
        await commit('SET_INFO_GRAFICO', { data: suc.data, tipoGrafico: tipoGrafico })
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
