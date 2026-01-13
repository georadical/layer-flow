# 📋 Tareas Pendientes - Layer Flow

> **Última actualización**: 2026-01-13

Este archivo rastrea tareas pendientes, mejoras y elementos por revisar en el proyecto Layer Flow.

---

## 🔴 Prioridad Alta

### Backend

- [ ] **Investigar error 401 en `/api/v1/logout`**
  - **Descripción**: El endpoint de logout devuelve `401 Unauthorized` cuando se llama
  - **Impacto**: Bajo (el logout funciona en frontend, pero genera errores en logs)
  - **Cuándo**: Antes de producción
  - **Contexto**: Ver [walkthrough.md](file:///C:/Users/geoal/.gemini/antigravity/brain/2bc8954c-085b-48c3-ad6d-9ceffd92e778/walkthrough.md) - Test 3

- [ ] **Limpiar archivos de debug del backend**
  - **Archivos**: `debug_config_loading.py`, `debug_result.txt`, `debug_test.py`, `error_log.txt`
  - **Ubicación**: `backend/`
  - **Cuándo**: Próximo commit
  - **Contexto**: Archivos temporales que quedaron de debugging

---

## 🟡 Prioridad Media

### Frontend

- [ ] **Migrar de localStorage a HTTP-only cookies**
  - **Descripción**: Cambiar almacenamiento de JWT de `localStorage` a cookies para mejor seguridad
  - **Beneficio**: Protección contra XSS, middleware server-side funcional
  - **Impacto**: Requiere cambios en backend y frontend
  - **Cuándo**: Antes de producción
  - **Contexto**: Ver limitación #1 en walkthrough.md

- [ ] **Implementar refresh tokens**
  - **Descripción**: Sistema de tokens de acceso + refresh para sesiones más largas
  - **Beneficio**: Mejor UX (usuarios no tienen que re-autenticarse frecuentemente)
  - **Cuándo**: Después de migrar a cookies
  - **Dependencias**: Requiere endpoints backend nuevos

### General

- [ ] **Push commits pendientes a origin**
  - **Descripción**: La rama local está adelante de `origin/main`
  - **Cuándo**: Próxima sesión de trabajo
  - **Comando**: `git push origin main`

---

## 🟢 Prioridad Baja (Mejoras UX/UI)

### Frontend

- [ ] **Mejorar diseño visual del frontend**
  - **Descripción**: Reemplazar estilos inline con diseño moderno y profesional
  - **Páginas afectadas**: `/login`, `/signup`, `/dashboard`
  - **Cuándo**: Cuando la funcionalidad core esté completa
  - **Sugerencias**: 
    - Usar biblioteca de componentes (shadcn/ui, MUI, etc.)
    - Implementar tema dark/light
    - Añadir animaciones y transiciones

- [ ] **Añadir loading skeletons**
  - **Descripción**: Reemplazar texto "Loading..." con skeleton screens
  - **Beneficio**: Mejor percepción de velocidad
  - **Cuándo**: Durante rediseño UI

- [ ] **Implementar toast notifications**
  - **Descripción**: Feedback visual para acciones (login exitoso, errores, etc.)
  - **Biblioteca sugerida**: `react-hot-toast` o `sonner`
  - **Cuándo**: Durante rediseño UI

- [ ] **Añadir funcionalidad "Remember Me"**
  - **Descripción**: Checkbox para sesiones persistentes más largas
  - **Cuándo**: Después de implementar refresh tokens

---

## 🔵 Funcionalidades Futuras

### Autenticación

- [ ] **Implementar verificación de email**
  - **Descripción**: Enviar email de confirmación al registrarse
  - **Requiere**: Servicio de email (SendGrid, AWS SES, etc.)
  - **Cuándo**: Antes de lanzar a producción con usuarios reales
  - **Contexto**: Actualmente signup emite JWT inmediatamente

- [ ] **Recuperación de contraseña**
  - **Descripción**: Flow de "Forgot Password"
  - **Requiere**: Servicio de email
  - **Cuándo**: Cuando haya usuarios reales

- [ ] **Autenticación de dos factores (2FA)**
  - **Descripción**: Capa adicional de seguridad
  - **Cuándo**: Para cuentas enterprise o premium

### OAuth

- [ ] **Completar implementación de OAuth callbacks**
  - **Descripción**: Verificar que los callbacks de Google/Microsoft/GitHub funcionen
  - **Ubicación**: `frontend/src/app/auth/`
  - **Cuándo**: Cuando se necesite OAuth en producción

---

## 📝 Notas de Mantenimiento

### Cuándo revisar este archivo:
- ✅ Al inicio de cada sesión de desarrollo
- ✅ Antes de hacer commits importantes
- ✅ Antes de deployar a producción
- ✅ Cuando se complete una tarea (para marcarla como `[x]`)

### Cómo usar este archivo:
1. **Marcar tareas completadas**: Cambiar `[ ]` a `[x]`
2. **Añadir nuevas tareas**: Agregar bajo la sección de prioridad apropiada
3. **Eliminar tareas obsoletas**: Borrar líneas de tareas que ya no aplican
4. **Actualizar fecha**: Cambiar "Última actualización" al modificar el archivo

---

## 🗑️ Tareas Completadas (Historial Reciente)

- [x] ~~Implementar Auth Context en frontend~~ (2026-01-12)
- [x] ~~Crear endpoint `/users/me` en backend~~ (2026-01-12)
- [x] ~~Refactorizar páginas de login/signup/dashboard~~ (2026-01-12)
- [x] ~~Añadir protección de rutas client-side~~ (2026-01-12)
- [x] ~~Probar flujos de signup/login/logout~~ (2026-01-12)

---

## 🔗 Referencias

- [Walkthrough de mejoras de autenticación](file:///C:/Users/geoal/.gemini/antigravity/brain/2bc8954c-085b-48c3-ad6d-9ceffd92e778/walkthrough.md)
- [Plan de implementación](file:///C:/Users/geoal/.gemini/antigravity/brain/2bc8954c-085b-48c3-ad6d-9ceffd92e778/implementation_plan.md)
