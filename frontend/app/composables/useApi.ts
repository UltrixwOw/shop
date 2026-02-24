export const useApi = () => {
  const config = useRuntimeConfig()
  
  const get = async (url: string) => {
    const res = await $fetch(`${config.public.apiBase}/${url}`, {
      credentials: 'include'
    })
    return res
  }

  const post = async (url: string, data: any, token?: string) => {
    const res = await $fetch(`${config.public.apiBase}/${url}`, {
      method: 'POST',
      body: data,
      headers: token ? { Authorization: `Bearer ${token}` } : {},
      credentials: 'include'
    })
    return res
  }

  return { get, post }
}