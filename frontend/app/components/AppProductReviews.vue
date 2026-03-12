<script setup lang="ts">
import { useReviewsStore } from "~/stores/reviews";

const { requireAuth } = useRequireAuth();

function handleLike(reviewId: number) {
  requireAuth(() => reviews.likeReview(reviewId));
}

const props = defineProps<{
  productId: number;
}>();

const reviews = useReviewsStore();

watch(
  () => props.productId,
  (id) => {
    if (id) reviews.fetchReviews(id);
  },
  { immediate: true }
);

const sortItems = [
  { label: "Most helpful", value: "helpful" },
  { label: "Newest", value: "newest" },
  { label: "Highest rating", value: "rating_high" },
  { label: "Lowest rating", value: "rating_low" },
];

const selectedSort = computed({
  get() {
    return reviews.sort || "helpful";
  },
  set(value: string) {
    reviews.sort = value;
  },
});
</script>

<template>
  <div class="space-y-8">
    <!-- Rating summary -->
    <UCard>
      <div class="flex gap-8">
        <div class="text-center min-w-24">
          <p class="text-3xl font-bold">
            {{ reviews.averageRating }}
          </p>

          <p class="text-sm text-gray-500">{{ reviews.totalReviews }} reviews</p>
        </div>

        <!-- Rating breakdown -->
        <div class="flex-1 space-y-2">
          <div
            v-for="row in reviews.ratingBreakdown"
            :key="row.star"
            class="flex items-center gap-3"
          >
            <span class="text-sm w-10"> {{ row.star }}★ </span>

            <div class="flex-1">
              <UProgress
                :model-value="
                  reviews.totalReviews
                    ? Math.round((row.count / reviews.totalReviews) * 100)
                    : 0
                "
                :max="100"
                size="xs"
                color="primary"
              />
            </div>

            <span class="text-xs text-gray-500 w-6 text-right">
              {{ row.count }}
            </span>
          </div>
        </div>
      </div>
    </UCard>

    <!-- Sorting -->
    <div class="flex justify-end">
      <USelect
        v-model="selectedSort"
        :items="sortItems"
        size="sm"
        class="w-56"
        placeholder="Sort by"
      />
    </div>

    <!-- Reviews -->
    <div class="space-y-6">
      <UCard v-for="review in reviews.paginatedReviews" :key="review.id">
        <div class="flex justify-between items-center">
          <!-- Author -->
          <div class="flex items-center gap-3">
            <UAvatar :alt="review.user_name" size="sm" />

            <div>
              <div class="flex items-center gap-2">
                <span class="font-medium">
                  {{ review.user_name }}
                </span>

                <!-- Badge для отзыва пользователя -->
                <UBadge
                  v-if="review.is_mine"
                  color="primary"
                  variant="soft"
                  size="xs"
                  icon="i-lucide-user"
                >
                  Your review
                </UBadge>

                <UBadge
                  v-else-if="review.verified_purchase"
                  color="success"
                  variant="soft"
                  size="xs"
                  icon="i-lucide-badge-check"
                >
                  Verified purchase
                </UBadge>
              </div>

              <div class="text-xs text-gray-500">
                {{ new Date(review.created_at).toLocaleDateString() }}
              </div>
            </div>
          </div>

          <!-- Rating -->
          <div class="flex">
            <span class="text-yellow-500 font-medium px-2">⭐{{ review.rating }}</span>
          </div>
        </div>

        <!-- Comment -->
        <p class="mt-3 text-sm leading-relaxed">
          {{ review.comment }}
        </p>

        <div class="flex items-center justify-end mt-4">
          <!-- Like -->
          <UButton
            size="xs"
            variant="ghost"
            icon="i-lucide-thumbs-up"
            :color="review.liked_by_me ? 'primary' : 'gray'"
            @click="handleLike(review.id)"
          >
            {{ review.likes_count }}
          </UButton>

          <!-- Moderation -->
          <UBadge v-if="!review.is_approved" color="warning" variant="soft" size="xs">
            Pending moderation
          </UBadge>
        </div>
      </UCard>
      <UPagination
        v-if="reviews.totalReviews > reviews.perPage"
        v-model:page="reviews.page"
        :total="reviews.totalReviews"
        :items-per-page="reviews.perPage"
        size="sm"
        class="flex justify-center"
      />
      <div v-if="reviews.totalReviews > 4" class="text-sm text-gray-500 text-center">
        Showing {{ reviews.startItem }}–{{ reviews.endItem }} of
        {{ reviews.totalReviews }} reviews
      </div>
    </div>

    <!-- Просто вставляем AppAddReview - вся логика внутри него -->
    <AppAddReview :product-id="productId" />
  </div>
</template>
