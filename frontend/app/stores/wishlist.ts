// stores/wishlist.ts
import { defineStore } from 'pinia'

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
    const items = ref<number[]>([]) // массив ID товаров
    const fullItems = ref<WishlistItem[]>([]) // полные данные (если нужны)
    const loading = ref(false)
    const initialized = ref(false)

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
        // Обрабатываем разные форматы ответа
        const itemsData = data.results || data.items || data || []

        // Сохраняем полные данные
        fullItems.value = itemsData.map((item: any) => ({
            id: item.id,
            product: item.product,
            product_name: item.product_name,
            product_price: item.product_price,
            product_image: item.product_image,
            created_at: item.created_at
        }))

        // Сохраняем только ID для быстрого доступа
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

        const { $api } = useNuxtApp()
        loading.value = true

        try {
            const res = await $api.get<WishlistResponse>('/wishlist/')
            setWishlist(res.data)
        } catch (e) {
            console.error('Wishlist fetch error:', e)
            items.value = []
            fullItems.value = []
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

        // Оптимистичное обновление
        items.value.push(productId)

        try {
            const res = await $api.post('/wishlist/', { product: productId })

            // Если API вернул полные данные, добавляем их
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
                // Если данных нет, перезагружаем весь список
                await fetchWishlist()
            }
        } catch (e) {
            // Откат при ошибке
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

        // Оптимистичное обновление
        const backup = [...items.value]
        const backupFull = [...fullItems.value]

        items.value = items.value.filter(id => id !== productId)
        fullItems.value = fullItems.value.filter(i => i.product !== productId)

        try {
            await $api.delete(`/wishlist/${productId}/`)
        } catch (e) {
            // Откат при ошибке
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
    // LOCAL STORAGE (для неавторизованных)
    // =============================

    const loadLocal = () => {
        if (!import.meta.client) return

        try {
            const saved = localStorage.getItem('wishlist')
            if (saved) {
                items.value = JSON.parse(saved)
            }
        } catch {
            items.value = []
        }
    }

    const saveLocal = () => {
        if (!import.meta.client) return
        localStorage.setItem('wishlist', JSON.stringify(items.value))
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
    }

    return {
        items,
        fullItems,
        loading,
        initialized,
        shareInfo,

        totalCount,
        isEmpty,
        isInWishlist,

        fetchWishlist,
        addToWishlist,
        removeFromWishlist,
        toggleWishlist,
        clearWishlistState,

        fetchShareInfo,
        generateShare,
        disableShare,
        getShareUrl,

        loadLocal,
        saveLocal,
        setWishlist,
        $reset
    }
})