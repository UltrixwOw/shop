// stores/wishlist.ts
import { defineStore } from 'pinia'
import { useAuthStore } from './auth'

interface WishlistItem {
    id: number
    product: number
    product_name?: string
    product_price?: number
    product_image?: string
    created_at: string
}

interface WishlistResponse {
    results?: WishlistItem[]
    items?: WishlistItem[]
}

export const useWishlistStore = defineStore('wishlist', () => {
    const items = ref<number[]>([])
    const fullItems = ref<WishlistItem[]>([])
    const loading = ref(false)
    const initialized = ref(false)
    
    const authStore = useAuthStore()
    const isAuthenticated = computed(() => authStore.isAuthenticated)

    // =============================
    // COMPUTED
    // =============================

    const totalCount = computed(() => items.value.length)
    const isEmpty = computed(() => items.value.length === 0)

    const isInWishlist = (productId: number) => {
        return items.value.includes(productId)
    }

    // =============================
    // INTERNAL
    // =============================

    const setWishlist = (data: any) => {
        const itemsData = data.results || data.items || data || []
        fullItems.value = itemsData.map((item: any) => ({
            id: item.id,
            product: item.product,
            product_name: item.product_name,
            product_price: item.product_price,
            product_image: item.product_image,
            created_at: item.created_at
        }))
        items.value = fullItems.value.map(i => i.product)
        initialized.value = true
    }

    const findItem = (productId: number) => {
        return fullItems.value.find(i => i.product === productId)
    }

    // =============================
    // FETCH
    // =============================

    const fetchWishlist = async () => {
        if (loading.value) return

        try {
            const { $api } = useNuxtApp()
            loading.value = true

            const res = await $api.get<WishlistResponse>('/wishlist/')
            setWishlist(res.data)
        } catch (e: any) {
            if (e.response?.status === 401) {
                loadLocal()
            } else {
                console.error('Wishlist fetch error:', e)
                items.value = []
                fullItems.value = []
            }
        } finally {
            loading.value = false
        }
    }

    // =============================
    // ADD
    // =============================

    const addToWishlist = async (productId: number) => {
        if (isInWishlist(productId)) return

        const { $api } = useNuxtApp()
        items.value.push(productId)

        if (!isAuthenticated.value) {
            saveLocal()
            return
        }

        try {
            const res = await $api.post('/wishlist/', { product: productId })

            if (res.data?.id) {
                fullItems.value.push({
                    id: res.data.id,
                    product: res.data.product,
                    product_name: res.data.product_name,
                    product_price: res.data.product_price,
                    product_image: res.data.product_image,
                    created_at: res.data.created_at
                })
            } else {
                await fetchWishlist()
            }
            
            if (isAuthenticated.value) {
                saveLocal()
            }
        } catch (e: any) {
            if (e.response?.status === 401) {
                saveLocal()
                return
            }

            items.value = items.value.filter(id => id !== productId)
            console.error('Add to wishlist failed', e)
            throw e
        }
    }

    // =============================
    // REMOVE
    // =============================

    const removeFromWishlist = async (productId: number) => {
        if (!isInWishlist(productId)) return

        const { $api } = useNuxtApp()
        const backup = [...items.value]
        const backupFull = [...fullItems.value]

        items.value = items.value.filter(id => id !== productId)
        fullItems.value = fullItems.value.filter(i => i.product !== productId)

        if (!isAuthenticated.value) {
            saveLocal()
            return
        }

        try {
            await $api.delete(`/wishlist/${productId}/`)
            saveLocal()
        } catch (e: any) {
            if (e.response?.status === 401) {
                saveLocal()
                return
            }

            items.value = backup
            fullItems.value = backupFull
            console.error('Remove from wishlist failed', e)
            throw e
        }
    }

    // =============================
    // TOGGLE
    // =============================

    const toggleWishlist = async (productId: number) => {
        if (isInWishlist(productId)) {
            await removeFromWishlist(productId)
        } else {
            await addToWishlist(productId)
        }
    }

    // =============================
    // SYNC LOCAL TO SERVER
    // =============================

    const syncLocalToServer = async (removeMissing: boolean = true) => {
        if (!import.meta.client) return
        
        loadLocal()
        
        if (isAuthenticated.value) {
            const localItems = [...items.value]
            
            try {
                const { $api } = useNuxtApp()
                
                if (localItems.length > 0) {
                    
                    const response = await $api.post('/wishlist/sync/', {
                        product_ids: localItems,
                        remove_missing: removeMissing
                    })
                    
                    const serverItems = response.data.results || []
                    fullItems.value = serverItems.map((item: any) => ({
                        id: item.id,
                        product: item.product,
                        created_at: item.created_at
                    }))
                    items.value = fullItems.value.map(i => i.product)
                    
                    localStorage.removeItem('wishlist')
                    
                    return response.data
                } else {
                    await fetchWishlist()
                }
            } catch (e) {
                console.error('Failed to sync wishlist to server:', e)
                await fetchWishlist()
                throw e
            }
        }
    }

    // =============================
    // SHARE
    // =============================

    const shareInfo = ref<any>(null)

    const fetchShareInfo = async () => {
        if (!import.meta.client) return null

        const { $api } = useNuxtApp()

        try {
            const res = await $api.get('/wishlist/share/')
            shareInfo.value = res.data
            return res.data
        } catch (e) {
            console.error('Failed to fetch share info', e)
            return null
        }
    }

    const generateShare = async () => {
        if (!import.meta.client) {
            throw new Error('Cannot share on server')
        }

        const { $api } = useNuxtApp()

        try {
            const res = await $api.post('/wishlist/share/', { is_public: true })
            shareInfo.value = res.data
            return res.data
        } catch (e) {
            console.error('Failed to generate share link', e)
            throw e
        }
    }

    const disableShare = async () => {
        if (!import.meta.client) return

        const { $api } = useNuxtApp()

        try {
            await $api.post('/wishlist/share/', { is_public: false })
            shareInfo.value = null
        } catch (e) {
            console.error('Failed to disable share', e)
        }
    }

    const getShareUrl = (token: string) => {
        if (!token || !import.meta.client) return null
        return `${window.location.origin}/wishlist/share/${token}`
    }

    // =============================
    // LOCAL STORAGE
    // =============================

    const loadLocal = () => {
        if (!import.meta.client) return

        try {
            const saved = localStorage.getItem('wishlist')
            if (saved) {
                items.value = JSON.parse(saved)
            } else {
                items.value = []
            }
            fullItems.value = []
        } catch {
            items.value = []
        }
    }

    const saveLocal = () => {
        if (!import.meta.client) return
        localStorage.setItem('wishlist', JSON.stringify(items.value))
    }

    // =============================
    // INIT - вызывается из компонентов
    // =============================

    const init = async () => {
        if (!import.meta.client) return
        if (initialized.value) return
        
        if (isAuthenticated.value) {
            await syncLocalToServer()
        } else {
            loadLocal()
        }
    }

    // =============================
    // RESET
    // =============================

    const clearWishlistState = () => {
        items.value = []
        fullItems.value = []
        initialized.value = false
    }

    const $reset = () => {
        items.value = []
        fullItems.value = []
        saveLocal()
    }

    watch(() => authStore.isAuthenticated, async (newVal, oldVal) => {
        if (newVal && !oldVal) {
            await syncLocalToServer()
        } else if (!newVal && oldVal) {
            loadLocal()
        }
    })

    // Убираем автоматический вызов init()

    return {
        items,
        fullItems,
        loading,
        initialized,
        shareInfo,
        isAuthenticated,

        totalCount,
        isEmpty,
        isInWishlist,

        fetchWishlist,
        addToWishlist,
        removeFromWishlist,
        toggleWishlist,
        clearWishlistState,
        syncLocalToServer,

        fetchShareInfo,
        generateShare,
        disableShare,
        getShareUrl,

        loadLocal,
        saveLocal,
        setWishlist,
        init,
        $reset
    }
})