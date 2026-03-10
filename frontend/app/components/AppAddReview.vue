<script setup lang="ts">
import { useReviewsStore } from "~/stores/reviews";
import { useAuthStore } from "~/stores/auth";

const props = defineProps<{
  productId: number;
}>();

const reviews = useReviewsStore();
const auth = useAuthStore();

const rating = ref(5);
const comment = ref("");
const loading = ref(false);

const { $api } = useNuxtApp();
const toast = useToast();

const submit = async () => {
  if (!comment.value.trim()) {
    toast.add({
      title: "Error",
      description: "Please write a comment",
      color: "error",
    });
    return;
  }

  loading.value = true;

  try {
    // Django ожидает JSON по умолчанию
    const payload = {
      product: props.productId,
      rating: rating.value,
      comment: comment.value.trim(),
    };

    console.log("Sending payload:", payload);

    // Отправляем как JSON (Django REST Framework по умолчанию принимает JSON)
    const response = await $api.post("/reviews/", payload, {
      headers: {
        "Content-Type": "application/json",
      },
    });

    console.log("Response:", response);

    // Очищаем форму
    comment.value = "";
    rating.value = 5;

    toast.add({
      title: "Success",
      description: "Your review has been submitted",
      color: "success",
    });

    // Обновляем список отзывов
    await reviews.fetchReviews(props.productId);
  } catch (error: any) {
    console.error("Submit error:", error);
    console.error("Error response:", error.response?.data);

    // Показываем конкретную ошибку от Django
    const errorData = error.response?.data;

    let errorMessage = "Failed to submit review";

    if (typeof errorData === "string") {
      errorMessage = errorData;
    } else if (errorData?.detail) {
      errorMessage = errorData.detail;
    } else if (errorData?.message) {
      errorMessage = errorData.message;
    } else if (errorData && typeof errorData === "object") {
      // Если ошибка валидации полей
      const firstError = Object.values(errorData)[0];
      errorMessage = Array.isArray(firstError) ? firstError[0] : String(firstError);
    }

    toast.add({
      title: "Error",
      description: errorMessage,
      color: "error",
    });
  } finally {
    loading.value = false;
  }
};

// Проверяем, может пользователь уже оставил отзыв
const hasUserReview = computed(() => {
  return reviews.items?.some((r: any) => r.is_mine) ?? false;
});

// Проверяем, может пользователь купил товар (опционально)
const canReview = computed(() => {
  // Если пользователь уже оставил отзыв, то нельзя
  if (hasUserReview.value) return false;

  // Здесь можно добавить проверку покупки через отдельный эндпоинт
  return true;
});
</script>

<template>
  <div v-if="auth.isAuthenticated" class="space-y-4 pt-4">
    <div class="font-semibold text-gray-500">Leave a review</div>

    <!-- Предупреждение, если уже оставил отзыв -->
    <UAlert
      v-if="hasUserReview"
      color="neutral"
      variant="outline"
      title="You have already reviewed this product"
      description="You can only leave one review per product"
      icon="i-lucide-lightbulb"
      class="text-gray-500"
    />

    <template v-else>
      <!-- Stars rating -->
      <div class="flex gap-1 text-2xl cursor-pointer">
        <span
          v-for="n in 5"
          :key="n"
          @click="rating = n"
          class="transition-colors"
          :class="n <= rating ? 'text-yellow-400' : 'text-gray-300 hover:text-yellow-200'"
        >
          ★
        </span>
      </div>

      <UTextarea
        v-model="comment"
        placeholder="Share your experience with this product..."
        :rows="4"
        :maxlength="500"
        :disabled="loading"
        :ui="{
          root: 'w-full',
        }"
      />

      <div class="flex justify-between items-center">
        <span class="text-xs text-gray-500"> {{ comment.length }}/500 </span>

        <UButton
          :loading="loading"
          :disabled="!comment.trim()"
          @click="submit"
          color="primary"
        >
          Submit review
        </UButton>
      </div>
    </template>
  </div>

  <div v-else class="flex items-center text-sm text-gray-400 pt-4">
    <AppLoginButton />
    <span class="ml-1">to leave a review</span>
  </div>
</template>
