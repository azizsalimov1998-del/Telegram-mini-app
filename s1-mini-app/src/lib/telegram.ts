/**
 * Telegram Web App SDK Integration Utilities
 * Provides helpers for Telegram Mini App integration
 */

import { useEffect, useState } from 'react';

// Types
export interface TelegramUser {
  id: number;
  first_name: string;
  last_name?: string;
  username?: string;
  language_code?: string;
}

export interface InitData {
  query_id?: string;
  user?: TelegramUser;
  start_param?: string;
  auth_date?: number;
  hash?: string;
}

declare global {
  interface Window {
    Telegram?: {
      WebApp: {
        initData: string;
        initDataUnsafe: InitData;
        themeParams: {
          bg_color: string;
          text_color: string;
          hint_color: string;
          link_color: string;
          button_color: string;
          button_text_color: string;
        };
        colorScheme: 'light' | 'dark';
        platform: string;
        ready: () => void;
        expand: () => void;
        close: () => void;
        showMainButton: (text: string, callback?: () => void) => void;
        hideMainButton: () => void;
        showBackButton: (callback?: () => void) => void;
        hideBackButton: () => void;
        onEvent: (eventType: string, eventHandler: () => void) => void;
        offEvent: (eventType: string, eventHandler: () => void) => void;
        HapticFeedback: {
          impactOccurred: (style: 'light' | 'medium' | 'heavy') => void;
          notificationOccurred: (type: 'success' | 'warning' | 'error') => void;
          selectionChanged: () => void;
        };
      };
    };
  }
}

/**
 * Get Telegram Web App instance
 */
export function getTelegramWebApp() {
  if (typeof window !== 'undefined' && window.Telegram?.WebApp) {
    return window.Telegram.WebApp;
  }
  return null;
}

/**
 * Get current Telegram user from initData
 */
export function getTelegramUser(): TelegramUser | null {
  const webApp = getTelegramWebApp();
  if (webApp?.initDataUnsafe?.user) {
    return webApp.initDataUnsafe.user;
  }
  return null;
}

/**
 * Get authorization headers for API requests
 */
export function getTelegramAuthHeaders(): Record<string, string> {
  const webApp = getTelegramWebApp();
  if (webApp?.initData) {
    return {
      'X-Telegram-Init-Data': webApp.initData,
    };
  }
  return {};
}

/**
 * React hook to get Telegram user
 */
export function useTelegramUser() {
  const [user, setUser] = useState<TelegramUser | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const webApp = getTelegramWebApp();
    if (webApp) {
      setUser(webApp.initDataUnsafe.user || null);
      webApp.ready();
    }
    setLoading(false);
  }, []);

  return { user, loading };
}

/**
 * React hook to get Telegram theme
 */
export function useTelegramTheme() {
  const [theme, setTheme] = useState<{
    bgColor: string;
    textColor: string;
    hintColor: string;
    linkColor: string;
    buttonColor: string;
    buttonTextColor: string;
    colorScheme: 'light' | 'dark';
  } | null>(null);

  useEffect(() => {
    const webApp = getTelegramWebApp();
    if (webApp) {
      const params = webApp.themeParams;
      setTheme({
        bgColor: params.bg_color,
        textColor: params.text_color,
        hintColor: params.hint_color,
        linkColor: params.link_color,
        buttonColor: params.button_color,
        buttonTextColor: params.button_text_color,
        colorScheme: webApp.colorScheme,
      });
    }
  }, []);

  return theme;
}

/**
 * Telegram UI Buttons Helper
 */
export class TelegramButtons {
  /**
   * Show Main Button (big red button at bottom)
   */
  static showMainButton(text: string, onClick?: () => void) {
    const webApp = getTelegramWebApp();
    if (webApp) {
      webApp.showMainButton(text, onClick);
    }
  }

  /**
   * Hide Main Button
   */
  static hideMainButton() {
    const webApp = getTelegramWebApp();
    if (webApp) {
      webApp.hideMainButton();
    }
  }

  /**
   * Show Back Button (in header)
   */
  static showBackButton(onClick?: () => void) {
    const webApp = getTelegramWebApp();
    if (webApp) {
      webApp.showBackButton(onClick);
    }
  }

  /**
   * Hide Back Button
   */
  static hideBackButton() {
    const webApp = getTelegramWebApp();
    if (webApp) {
      webApp.hideBackButton();
    }
  }

  /**
   * Trigger haptic feedback
   */
  static hapticFeedback(
    type: 'impact' | 'notification' | 'selection',
    style?: 'light' | 'medium' | 'heavy' | 'success' | 'warning' | 'error'
  ) {
    const webApp = getTelegramWebApp();
    if (webApp?.HapticFeedback) {
      switch (type) {
        case 'impact':
          webApp.HapticFeedback.impactOccurred(style as any || 'light');
          break;
        case 'notification':
          webApp.HapticFeedback.notificationOccurred(style as any || 'success');
          break;
        case 'selection':
          webApp.HapticFeedback.selectionChanged();
          break;
      }
    }
  }
}

/**
 * Initialize Telegram Web App
 */
export function initTelegramWebApp() {
  const webApp = getTelegramWebApp();
  if (webApp) {
    webApp.ready();
    webApp.expand();
    return true;
  }
  return false;
}
