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

export function giphySearchSingleApi(giphyId) {
  const url = `${path}/giphy/search/${giphyId}`;
  return axios({
    method: 'get',
    url,
  });
}

export function addTagToGiphyApi(payload, jwt) {
  const url = `${path}/tags/${payload.giphyId}/${payload.tag}`;
  const headers = { Authorization: `Bearer: ${jwt}` };
  return axios({
    method: 'post',
    url,
    headers,
  });
}

export function getTagsToGiphyApi(giphyId, jwt) {
  const url = `${path}/tags/${giphyId}`;
  const headers = { Authorization: `Bearer: ${jwt}` };
  return axios({
    method: 'get',
    url,
    headers,
  });
}

export function removeTagFromGiphyApi(payload, jwt) {
  const url = `${path}/tags/${payload.giphyId}/${payload.tag}`;
  const headers = { Authorization: `Bearer: ${jwt}` };
  return axios({
    method: 'delete',
    url,
    headers,
  });
}

export function saveUserGiphyApi(giphyId, jwt) {
  const url = `${path}/user/giphy/${giphyId}`;
  const headers = { Authorization: `Bearer: ${jwt}` };
  return axios({
    method: 'post',
    url,
    headers,
  });
}

export function deleteUserGiphyApi(giphyId, jwt) {
  const url = `${path}/user/giphy/${giphyId}`;
  const headers = { Authorization: `Bearer: ${jwt}` };
  return axios({
    method: 'delete',
    url,
    headers,
  });
}

export function getUserGiphiesApi(jwt) {
  const url = `${path}/user/giphy`;
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
