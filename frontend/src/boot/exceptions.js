import { Loading, Notify } from 'quasar'

const handleError = async (err) => {
  Loading.hide()
  err = await err
  // console.log(err.response.data)
  // console.log(err.response.status)
  var message = ''
  if (err.message === 'Network Error') {
    message = 'Sem internet'
  } else if (err.response.status === 500) {
    message = 'Erro no servidor'
  } else {
    const key = Object.keys(err.response.data)[0]
    const value = Object.values(err.response.data)[0]
    message = key + ': ' + value
  }

  Notify.create({
    type: 'negative',
    message: message
  })
}

export {
  handleError
}
