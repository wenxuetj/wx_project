import axios from 'axios'
var baseUrl = '/api'

export const loginRequest = params => { return axios.get((baseUrl + '/loginHandler'), params) }

export const getUnitList = params => { return axios.get((baseUrl + '/unit/list'), { params: params }) }
export const saveUnit = params => { return axios.post((baseUrl + '/unit/save'), { params: params }) }
export const deleteUnit = params =>{ return axios.post((baseUrl + '/unit/delete'), {params: params}) }
