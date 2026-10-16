window.aui.amd_define('@amzn/aui-overlays.functions', ['@amzn/flow.routing-kata-functions'], (function (require$$0) { 'use strict';

	var commonjsGlobal = typeof globalThis !== 'undefined' ? globalThis : typeof window !== 'undefined' ? window : typeof global !== 'undefined' ? global : typeof self !== 'undefined' ? self : {};

	var _public = {};

	var __importDefault = (commonjsGlobal && commonjsGlobal.__importDefault) || function (mod) {
	    return (mod && mod.__esModule) ? mod : { "default": mod };
	};
	Object.defineProperty(_public, "__esModule", { value: true });
	const flow_routing_kata_functions_1 = __importDefault(require$$0);
	let activeDismissableToast = null;
	function clearActiveDismissableToast() {
	    const toast = activeDismissableToast;
	    activeDismissableToast = null;
	    toast === null || toast === void 0 ? void 0 : toast.invalidate();
	}
	function activateDismissableToast(toast) {
	    if (activeDismissableToast !== toast) {
	        clearActiveDismissableToast();
	    }
	    activeDismissableToast = toast;
	}
	const functionBag = (_context) => {
	    return {
	        createModal: (template, options) => {
	            window.P.when('A', 'a-modal', 'ready').execute(`a-modal-create-${template}`, function (A, modal) {
	                const preloadContent = A.$(`[k-preload-id="${template}"]`);
	                const trigger = A.$(`[id="${template}-trigger"]`);
	                const preloadContentId = `a-popover-${template}`;
	                // only set id for the first matched element
	                if (preloadContent.length === 1) {
	                    preloadContent.prop('id', preloadContentId);
	                }
	                const triggerId = `a-modal-trigger-${template}`;
	                // only set id for the first matched element
	                if (trigger.length === 1) {
	                    trigger.prop('id', triggerId);
	                }
	                const params = {
	                    name: template,
	                    popoverLabel: options.popoverLabel,
	                    header: options.header,
	                    width: options.width,
	                    height: options.height,
	                };
	                modal.create(trigger, params);
	            });
	            return {
	                // unused value; trigger id is provided by the server-side implementation
	                triggerId: '',
	                show: () => {
	                    window.P.when('a-modal', 'ready').execute(`a-modal-show-${template}`, function (modal) {
	                        var createdModal = modal.get(template);
	                        if (createdModal && createdModal.show)
	                            createdModal.show();
	                    });
	                },
	                hide: () => {
	                    window.P.when('a-modal', 'ready').execute(`a-modal-hide-${template}`, function (modal) {
	                        var createdModal = modal.get(template);
	                        if (createdModal && createdModal.hide)
	                            createdModal.hide();
	                    });
	                },
	            };
	        },
	        createPopover: (template, options) => {
	            window.P.when('A', 'a-popover', 'ready').execute(`a-popover-create-${template}`, function (A, popover) {
	                const preloadContent = A.$(`[k-preload-id="${template}"]`);
	                const triggerById = A.$(`[id="${template}-trigger"]`);
	                const triggerByCustomAttr = A.$(`[a-popover-trigger-id="${template}-trigger"]`);
	                const trigger = triggerById.length > 0 ? triggerById : triggerByCustomAttr;
	                const preloadContentId = `a-popover-${template}`;
	                // only set id for the first matched element
	                if (preloadContent.length === 1) {
	                    preloadContent.prop('id', preloadContentId);
	                }
	                const triggerId = `a-popover-trigger-${template}`;
	                // only set id for the first matched element
	                if (trigger.length === 1) {
	                    trigger.prop('id', triggerId);
	                }
	                const positionMap = {
	                    top: 'triggerTop',
	                    bottom: 'triggerBottom',
	                    left: 'triggerLeft',
	                    right: 'triggerRight',
	                };
	                const params = {
	                    name: template,
	                    popoverLabel: options.popoverLabel,
	                    closeButtonLabel: options.closeButtonLabel,
	                    header: options.header,
	                    activate: options.activate == 'press' ? 'onclick' : 'onmouseover',
	                    position: options.position ? positionMap[options.position] : undefined,
	                };
	                popover.create(trigger, params);
	            });
	            return {
	                // unused value; trigger id is provided by the server-side implementation
	                triggerId: '',
	            };
	        },
	        createBottomSheet: (template, options) => {
	            window.P.when('A', 'a-sheet', 'ready').execute(`a-sheet-create-${template}`, function (A, bottomSheet) {
	                const preloadContent = A.$(`[k-preload-id="${template}"]`);
	                const preloadContentId = `a-bottomsheet-content-${template}`;
	                // only set id for the first matched element
	                if (preloadContent.length === 1) {
	                    preloadContent.prop('id', preloadContentId);
	                }
	                const params = {
	                    name: `a-bottomsheet-name-${template}`,
	                    preloadDomId: preloadContentId,
	                    heading: options.header,
	                    height: options.height,
	                    closeType: 'icon',
	                    sheetLabel: options.sheetLabel,
	                    sheetDescription: options.sheetDescription,
	                };
	                bottomSheet.create(params);
	            });
	            return {
	                show: () => {
	                    window.P.when('a-sheet', 'ready').execute(`a-sheet-show-${template}`, function (bottomSheet) {
	                        bottomSheet.get(`a-bottomsheet-name-${template}`).show();
	                    });
	                },
	                hide: () => {
	                    window.P.when('a-sheet', 'ready').execute(`a-sheet-hide-${template}`, function (bottomSheet) {
	                        bottomSheet.get(`a-bottomsheet-name-${template}`).hide();
	                    });
	                },
	            };
	        },
	        generateUniqueId: () => {
	            return '';
	        },
	        createToast: (content, options) => {
	            createStaticToast(content, options, {
	                onBeforeShow: clearActiveDismissableToast,
	            });
	        },
	        createDismissableToast: (content, options) => {
	            const toastController = createStaticToast(content, options, {
	                trackDismissal: true,
	                onBeforeShow: activateDismissableToast,
	                onInactive: inactiveToast => {
	                    if (activeDismissableToast === inactiveToast) {
	                        activeDismissableToast = null;
	                    }
	                },
	            });
	            return toastController.dismiss;
	        },
	    };
	};
	function createStaticToast(content, options, lifecycle = {}) {
	    const toastId = `toast-${Date.now()}-${Math.random().toString(36).slice(2, 11)}`;
	    let toastInstance = null;
	    let inactive = false;
	    let removeDismissedListener = null;
	    let removeInteractionListener = null;
	    const markInactive = () => {
	        var _a;
	        if (inactive) {
	            return;
	        }
	        inactive = true;
	        removeDismissedListener === null || removeDismissedListener === void 0 ? void 0 : removeDismissedListener();
	        removeDismissedListener = null;
	        removeInteractionListener === null || removeInteractionListener === void 0 ? void 0 : removeInteractionListener();
	        removeInteractionListener = null;
	        toastInstance = null;
	        (_a = lifecycle.onInactive) === null || _a === void 0 ? void 0 : _a.call(lifecycle, controller);
	    };
	    const controller = {
	        id: toastId,
	        dismiss: () => {
	            if (inactive) {
	                return;
	            }
	            const instance = toastInstance;
	            markInactive();
	            instance === null || instance === void 0 ? void 0 : instance.dismiss();
	        },
	        invalidate: markInactive,
	    };
	    window.P.when('A', 'a-toast', 'ready').execute(`a-toast-create-${toastId}`, function (A, toast) {
	        var _a;
	        if (inactive) {
	            return;
	        }
	        const instance = new toast(Object.assign(Object.assign(Object.assign(Object.assign({}, (lifecycle.trackDismissal ? { name: toastId } : {})), { content: buildWebToastContent(content, lifecycle.trackDismissal ? markInactive : undefined, lifecycle.trackDismissal ? toastId : undefined), label: options.toastLabel }), (options.closeButtonLabel ? { closeButtonLabel: options.closeButtonLabel } : {})), (options.timeout !== undefined ? { timeout: options.timeout } : {})));
	        toastInstance = instance;
	        (_a = lifecycle.onBeforeShow) === null || _a === void 0 ? void 0 : _a.call(lifecycle, controller);
	        if (inactive) {
	            return;
	        }
	        if (lifecycle.trackDismissal) {
	            const dismissedEventName = `a:stickyToast:${toastId}:dismissed`;
	            const onDismissed = () => markInactive();
	            A.one(dismissedEventName, onDismissed);
	            removeDismissedListener = () => A.off(dismissedEventName, onDismissed);
	            if (typeof content !== 'string' && content.linkData) {
	                const onDocumentClick = (event) => {
	                    if (!(event.target instanceof Element)) {
	                        return;
	                    }
	                    const link = event.target.closest(`[data-aui-overlays-toast-id="${toastId}"]`);
	                    if (!link) {
	                        return;
	                    }
	                    Promise.resolve().then(() => {
	                        if (!document.contains(link)) {
	                            markInactive();
	                        }
	                    });
	                };
	                document.addEventListener('click', onDocumentClick, true);
	                removeInteractionListener = () => document.removeEventListener('click', onDocumentClick, true);
	            }
	        }
	        instance.show();
	    });
	    return controller;
	}
	function buildWebToastContent(content, onInteraction, interactionId) {
	    if (typeof content === 'string') {
	        return content;
	    }
	    return {
	        message: content.message,
	        linkData: content.linkData
	            ? buildWebLinkData(content.linkData, onInteraction, interactionId)
	            : undefined,
	    };
	}
	// Map our linkData to AUI3 a-toast linkData. AUI3 accepts either `callback`
	// (a handler run on tap, e.g. to open an a-sheet) or `href` (navigation). We
	// prefer callback when provided; otherwise resolve the route to an href.
	function buildWebLinkData(linkData, onInteraction, interactionId) {
	    const interactionData = interactionId ? { 'data-aui-overlays-toast-id': interactionId } : {};
	    if (typeof linkData.callback === 'function') {
	        const callback = linkData.callback;
	        return Object.assign(Object.assign({ text: linkData.text }, interactionData), { callback: onInteraction
	                ? () => {
	                    callback();
	                    onInteraction();
	                }
	                : callback });
	    }
	    if (linkData.route) {
	        return Object.assign(Object.assign({ text: linkData.text }, interactionData), { href: (0, flow_routing_kata_functions_1.default)().resolveUrl(linkData.route) || '#' });
	    }
	    return undefined;
	}
	var _default = _public.default = functionBag;

	return _default;

}));
