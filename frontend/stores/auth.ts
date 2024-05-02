import { defineStore } from 'pinia'
import nuxt from 'nuxt'

const _15MIN = 15 * 60 * 1000;

export const useAuthStore = defineStore('auth', () => {
    const authenticated = ref(false)
    const loading = ref(false)
    const userInfo = ref({
        id: 0,
        username: '',
        email: '',
        nickname: '',
        image: '',
        lastUpdate: new Date()
    })

    const token = useCookie('token')
    const refreshToken = useCookie('refreshToken')
    const config = useRuntimeConfig()
    const BASE_URL = config.public.BASE_URL

    if(token.value) {
        authenticated.value = true
    }

    const getUserMeta = async() => {
        loading.value = true;
        const response: {id: number, username: string, email: string, nickname: string, image: string}  = await $fetch(`${BASE_URL}/users/profile/`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token.value}`
            }
        })
        if(response) {
            userInfo.value = {
                id: response.id,
                email: response.email,
                image: response.image,
                nickname: response.nickname,
                username: response.username,
                lastUpdate: new Date()
            }
        } else {
            token.value = null
            refreshToken.value = null
            authenticated.value = false

            await refresh()
            await getUserMeta()
        }
    }

    const authUser = async (payload: {username: string, password: string}) => {
        loading.value = true;
        const response: {access: string, refresh: string} = await $fetch(`${BASE_URL}/users/login/`,  {
            method: 'POST',
            body:{
                username: payload.username,
                password: payload.password
            }
        })
        loading.value = false
        if (!response) {
            throw Error()
        } else {
            token.value = response.access
            refreshToken.value = response.refresh
            authenticated.value = true
            await getUserMeta()
        }
        loading.value = false
    }
    const logout = async () => {
        loading.value = true
            // @ts-ignore
        const response = await $fetch(`${BASE_URL}/users/logout/`, {
            headers: {
                'Authorization': `Bearer ${token.value}`
            }
        })
        loading.value = false
        authenticated.value = false
        token.value = null
        loading.value = false
        userInfo.value = {
            id: 0,
            email: '',
            username: '',
            image: '',
            nickname: '',
            lastUpdate: new Date()
        }
    };

    const refresh = async () => {
        if(new Date().getTime() < userInfo.value.lastUpdate.getTime() + _15MIN)
            return

        loading.value = true
        // @ts-ignore
        const response: {access: string, refresh: string} = await $fetch(`${BASE_URL}/users/login/refresh/`,{
            method: 'POST',
            body: {
                refresh: refreshToken.value
            },
            headers: {
                'Authorization': `Bearer ${token.value}`
            }
        })

        if(response) {
            token.value = response.access
            refreshToken.value = response.refresh
            userInfo.value.lastUpdate = new Date()
        } else {
            token.value = null
            refreshToken.value = null
            authenticated.value = false
        }

        loading.value = false
    }

    return {authenticated, loading, authUser, logout, token, refreshToken, refresh, userInfo, getUserMeta }
})