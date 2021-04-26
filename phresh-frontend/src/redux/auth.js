import initialState from "./initialState"
import axios from "axios" 

export const REQUEST_LOGIN = "@@auth/REQUEST_LOGIN"
export const REQUEST_LOGIN_FAILURE = "@@auth/REQUEST_LOGIN_FAILURE"
export const REQUEST_LOGIN_SUCCESS = "@@auth/REQUEST_LOGIN_SUCCESS"
export const REQUEST_LOG_USER_OUT = "@@auth/REQUEST_LOG_USER_OUT"

export default function authReducer(state = initialState.auth, action = {}) {
  switch (action.type) {
    case REQUEST_LOGIN:
      return {
        ...state,
        isLoading: true,
      }
    case REQUEST_LOGIN_FAILURE:
      return {
        ...state,
        isLoading: false,
        error: action.error,
        user: {},
      }
    case REQUEST_LOGIN_SUCCESS:
      return {
        ...state,
        isLoading: false,
        error: null,
      }
    case REQUEST_LOG_USER_OUT:
      return {
        ...initialState.auth,
      }
    default:
      return state
  }
}

export const Actions = {}

Actions.requestUserLogin = ({ email, password }) => {
  return async (dispatch) => {
    // set redux state to loading while we wait for server response
    dispatch({ type: REQUEST_LOGIN })
    // create the url-encoded form data
    const formData = new FormData()
    formData.set("username", email)
    formData.set("password", password)
    // set the request headers
    const headers = {
      "Content-Type": "application/x-www-form-urlencoded",
    }
    try {
      // make the actual HTTP request to our API
      const res = await axios({
        method: `POST`,
        url: `http://localhost:8000/api/users/login/token/`,
        data: formData,
        headers,
      })
      console.log(res)
      // stash the access_token our server returns
      const access_token = res?.data?.access_token
      localStorage.setItem("access_token", access_token)
      // dispatch the success action
      return dispatch({ type: REQUEST_LOGIN_SUCCESS })
    } catch (error) {
      console.log(error)
      // dispatch the failure action
      return dispatch({ type: REQUEST_LOGIN_FAILURE, error: error?.message })
    }
  }
}

Actions.logUserOut = () => {
  return { type: REQUEST_LOG_USER_OUT }
}

