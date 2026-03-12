import { defineStore } from 'pinia'

interface Review {
  id: number
  product: number
  user_name: string
  rating: number
  comment: string
  likes_count: number
  liked_by_me: boolean
  is_approved: boolean
  created_at: string
  is_mine?: boolean // Добавим опциональное поле
}

export const useReviewsStore = defineStore('reviews', () => {

  const items = ref<Review[]>([])
  const loading = ref(false)
  const initialized = ref(false)
  const sort = ref("helpful") // Это есть

  const { $api } = useNuxtApp()

  // =============================
  // FETCH REVIEWS
  // =============================

  const fetchReviews = async (productId: number): Promise<Review[]> => {

    loading.value = true

    try {

      const res = await $api.get<Review[]>(`/reviews/?product=${productId}`)

      items.value = res.data
      initialized.value = true

      return res.data

    } finally {
      loading.value = false
    }

  }

  // =============================
  // LIKE REVIEW
  // =============================

  const likeReview = async (reviewId: number) => {

    const res = await $api.post(`/reviews/${reviewId}/like/`)

    const review = items.value.find(r => r.id === reviewId)

    if (review) {
      review.likes_count = res.data.likes_count
      review.liked_by_me = res.data.liked
    }

  }

  // =============================
  // STATS
  // =============================

  const averageRating = computed(() => {

    if (!items.value.length) return 0

    const sum = items.value.reduce((acc, r) => acc + r.rating, 0)

    return Number((sum / items.value.length).toFixed(1))

  })

  const totalReviews = computed(() => items.value.length)

  // ⭐ rating breakdown
  const ratingBreakdown = computed(() => {
    const breakdown = [5, 4, 3, 2, 1].map((star) => ({
      star,
      count: items.value.filter((r) => r.rating === star).length,
    }));

    return breakdown;
  });

  // =============================
  // SORTING
  // =============================

  const sortedReviews = computed(() => {
    const list = [...items.value];

    if (sort.value === "newest") {
      return list.sort(
        (a, b) =>
          new Date(b.created_at).getTime() -
          new Date(a.created_at).getTime()
      );
    }

    if (sort.value === "rating_high") {
      return list.sort((a, b) => b.rating - a.rating);
    }

    if (sort.value === "rating_low") {
      return list.sort((a, b) => a.rating - b.rating);
    }

    // helpful
    return list.sort((a, b) => b.likes_count - a.likes_count);
  });

  // =============================
  // RESET
  // =============================

  const $reset = () => {

    items.value = []
    initialized.value = false

  }

  // =============================
  // PAGINATION
  // =============================

  const page = ref(1)
  const perPage = 4

  const paginatedReviews = computed(() => {
    const start = (page.value - 1) * perPage
    const end = start + perPage

    return sortedReviews.value.slice(start, end)
  })

  const startItem = computed(() => {
    if (!totalReviews.value) return 0
    return (page.value - 1) * perPage + 1
  })

  const endItem = computed(() => {
    return Math.min(page.value * perPage, totalReviews.value)
  })

  watch(sort, () => {
    page.value = 1
  })

  return {
    items,
    loading,
    initialized,
    sort,
    page,
    perPage,
    averageRating,
    ratingBreakdown,
    sortedReviews,
    paginatedReviews,
    totalReviews,
    startItem,
    endItem,
    fetchReviews,
    likeReview,
    $reset
  }

})