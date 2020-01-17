import axios from 'axios';

const path = process.env.VUE_APP_BASE_URL;

export function giphySearchApi(data) {
  const url = `${path}/giphy/search`;
  return axios({
    method: 'post',
    url,
    data,
  });
}

export function saveUserGiphyApi(giphyId, jwt) {
  const url = `${path}/giphy/user/${giphyId}`;
  const headers = { Authorization: `Bearer: ${jwt}` };
  return axios({
    method: 'post',
    url,
    headers,
  });
}

export function deleteUserGiphyApi(giphyId, jwt) {
  const url = `${path}/giphy/user/${giphyId}`;
  const headers = { Authorization: `Bearer: ${jwt}` };
  return axios({
    method: 'delete',
    url,
    headers,
  });
}

export function getUserGiphiesApi(jwt) {
  const url = `${path}/giphy/user`;
  const headers = { Authorization: `Bearer: ${jwt}` };
  return axios({
    method: 'get',
    url,
    headers,
  });
}

export function getUserInfoApi(jwt) {
  const headers = { Authorization: `Bearer: ${jwt}` };
  const url = `${path}/user/info`;
  return axios({
    method: 'get',
    url,
    headers,
  });
}

export function loginUserApi(data) {
  const url = `${path}/user/login`;
  return axios({
    method: 'post',
    url,
    data,
  });
}

export function registerUserApi(data) {
  const url = `${path}/user/register`;
  return axios({
    method: 'post',
    url,
    data,
  });
}
