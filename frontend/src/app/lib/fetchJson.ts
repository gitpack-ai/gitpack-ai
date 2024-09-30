

export class FetchError extends Error {
    response: Response
    data: any
    constructor({
      message,
      response,
      data,
    }: {
      message: string
      response: Response
      data: any
    }) {
      // Pass remaining arguments (including vendor specific ones) to parent constructor
      super(message)
  
      // Maintains proper stack trace for where our error was thrown (only available on V8)
      if (Error.captureStackTrace) {
        Error.captureStackTrace(this, FetchError)
      }
  
      this.name = 'FetchError'
      this.response = response
      this.data = data ?? { message: message }
    }
}
  
export default async function fetchJson<JSON = unknown>(
  input: string,
  init?: RequestInit
): Promise<JSON> {
    const auth_token = localStorage.getItem('authToken');
    let updatedInit = {
      ...init,
      credentials: 'include',
      headers: {
        ...init?.headers,
        'Content-Type': 'application/json'
      },
    };
    if(auth_token !== '' && auth_token !== undefined && auth_token !== null){
      // @ts-ignore
      updatedInit.headers.Authorization = `Token ${auth_token}`;
    }
    // @ts-ignore
    const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}${input}`, updatedInit);
    // if the server replies, there's always some data in json
    // if there's a network error, it will throw at the previous line
    const data = await response.json()
  
    // response.ok is true when res.status is 2xx
    // https://developer.mozilla.org/en-US/docs/Web/API/Response/ok
    if (response.ok) {
      return data
    }
  
    throw new FetchError({
      message: response.statusText,
      response,
      data,
    })
  }