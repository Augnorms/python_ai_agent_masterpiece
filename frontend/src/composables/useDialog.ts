import { ref } from 'vue'

export interface DialogOptions {
  title?: string
  message: string
  type?: 'info' | 'warning' | 'error' | 'success' | 'confirm'
  confirmText?: string
  cancelText?: string
  showCancel?: boolean
}

const isDialogOpen = ref(false)
const dialogOptions = ref<DialogOptions>({
  title: 'System Notice',
  message: '',
  type: 'info',
  confirmText: 'Acknowledge',
  cancelText: 'Cancel',
  showCancel: false
})

let resolvePromise: ((value: boolean) => void) | null = null

export function useDialog() {
  const show = (options: DialogOptions | string): Promise<boolean> => {
    if (typeof options === 'string') {
      dialogOptions.value = {
        title: 'System Notice',
        message: options,
        type: 'info',
        confirmText: 'Acknowledge',
        cancelText: 'Cancel',
        showCancel: false
      }
    } else {
      const isConfirm = options.type === 'confirm' || options.showCancel === true
      dialogOptions.value = {
        title: options.title || (isConfirm ? 'Security Confirmation' : 'System Notice'),
        message: options.message,
        type: options.type || (isConfirm ? 'confirm' : 'info'),
        confirmText: options.confirmText || (isConfirm ? 'Confirm' : 'Acknowledge'),
        cancelText: options.cancelText || 'Cancel',
        showCancel: options.showCancel ?? isConfirm
      }
    }

    isDialogOpen.value = true

    return new Promise<boolean>((resolve) => {
      resolvePromise = resolve
    })
  }

  const alert = (
    message: string,
    title: string = 'Security Dispatch Notice',
    type: DialogOptions['type'] = 'info'
  ): Promise<boolean> => {
    return show({
      title,
      message,
      type,
      showCancel: false,
      confirmText: 'Acknowledge'
    })
  }

  const confirm = (
    message: string,
    title: string = 'Security Confirmation',
    confirmText: string = 'Sign Out',
    cancelText: string = 'Cancel'
  ): Promise<boolean> => {
    return show({
      title,
      message,
      type: 'confirm',
      showCancel: true,
      confirmText,
      cancelText
    })
  }

  const handleConfirm = () => {
    isDialogOpen.value = false
    if (resolvePromise) {
      resolvePromise(true)
      resolvePromise = null
    }
  }

  const handleCancel = () => {
    isDialogOpen.value = false
    if (resolvePromise) {
      resolvePromise(false)
      resolvePromise = null
    }
  }

  return {
    isDialogOpen,
    dialogOptions,
    show,
    alert,
    confirm,
    handleConfirm,
    handleCancel
  }
}

