import { defineStore } from 'pinia'
import axios from "axios";

export const useAuthStore = defineStore('auth', () => {
    const authenticated = ref(false)
    const loading = ref(false)

    const token = useCookie('token')
    if(token.value) {
        authenticated.value = true
    }

    const authUser = async (payload: {username: string, password: string}) => {
        // @ts-ignore
        loading.value = true
        const response = await axios.post(`http://localhost:8000/users/login/`,  {
            username: payload.username,
            password: payload.password
        })
        loading.value = false
        if (response.data) {
            const refresh = useCookie('refresh')
            token.value = response.data.access
            refresh.value = response.data.refresh
            authenticated.value = true
        }
    }
    const logout = async () => {
        loading.value = true
        const token = useCookie('token')
        try {
            const response = await axios({
                baseURL: `http://localhost:8000/users/logout/`,
                headers: {
                    'Authorization': `JWT ${token.value}`
                },
                xsrfCookieName: 'csrftoken'
            })
            loading.value = false
            if (response.data) {
                authenticated.value = false
                token.value = null
            }
        } catch (e) {
            throw e
        }
    };

    return {authenticated, loading, authUser, logout }
})