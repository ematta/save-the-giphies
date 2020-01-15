import axios from 'axios';

const path = process.env.VUE_APP_BASE_URL;

export function giphySearch(data) {
  return axios({
    method: 'post',
    url: `${path}/giphy/search`,
    data,
  });
}

export function saveGif(data, jwt) {
  return axios({
    method: 'post',
    url: `${path}/giphy/save`,
    headers: { Authorization: `Bearer: ${jwt}` },
    data,
  });
}

export function authenticate(data) {
  return axios({
    method: 'post',
    url: `${path}/user/login`,
    data,
  });
}

export function register(data) {
  return axios({
    method: 'post',
    url: `${path}/user/register`,
    data,
  });
}
