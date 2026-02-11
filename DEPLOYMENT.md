# Guía de Despliegue - Keep Safe Operation

## 📋 Pre-requisitos
- Cuenta de GitHub
- Cuenta de Streamlit Cloud (conectada con GitHub)
- Dominio propio en Hostinger (opcional, para redirección)

## 🚀 Pasos para Desplegar

### 1. Preparar el Repositorio (✅ Ya completado)
- [x] `.gitignore` creado
- [x] `requirements.txt` actualizado
- [x] `README.md` completo
- [x] Configuración de Streamlit (`.streamlit/config.toml`)
- [x] Código sin información sensible

### 2. Subir a GitHub
```bash
# Si aún no has inicializado git:
git init
git add .
git commit -m "Preparar para despliegue en Streamlit Cloud"

# Si ya tienes un repositorio remoto:
git add .
git commit -m "Actualizar para despliegue"
git push origin main
```

### 3. Desplegar en Streamlit Cloud

1. Ve a [https://share.streamlit.io/](https://share.streamlit.io/)
2. Haz clic en "New app"
3. Selecciona tu repositorio privado
4. Configura:
   - **Repository**: `tu-usuario/Calculadora-KeepSafe`
   - **Branch**: `main` (o tu rama principal)
   - **Main file path**: `app.py`
5. Haz clic en "Deploy"

### 4. Verificar el Despliegue

- La app estará disponible en: `https://[nombre-app]-[usuario].streamlit.app`
- Verifica que todas las imágenes se carguen correctamente
- Prueba todos los cálculos y funcionalidades
- Revisa que el footer se visualice correctamente

### 5. Compartir el Link

Una vez desplegada, copia el link público y compártelo con tus clientes.

**Importante**: Aunque tu repositorio sea privado, la app será pública en el link generado. Sin embargo, **el código fuente NO es visible** para quienes accedan a la app.

---

## 🌐 Redirigir un Subdominio desde Hostinger a Streamlit Cloud

Si tienes un dominio en Hostinger y quieres que un subdominio (por ejemplo, `calculadora.tudominio.com`) apunte a tu app de Streamlit Cloud, sigue estos pasos:

### Pasos para redirigir un subdominio en Hostinger

1. Ingresa al panel de control de Hostinger.
2. Ve a la sección **Dominios** y selecciona tu dominio principal.
3. Busca la opción **Subdominios** y crea uno nuevo, por ejemplo: `calculadora.tudominio.com`.
4. Una vez creado, ve a la sección **Redirección** o **Redirects**.
5. Selecciona el subdominio creado y configura la redirección tipo **URL Redirect** (o similar) hacia la URL de tu app de Streamlit Cloud, por ejemplo:
   - `https://nombre-app-usuario.streamlit.app`
6. Guarda los cambios. La propagación puede tardar unos minutos.
7. ¡Listo! Ahora cuando alguien visite `calculadora.tudominio.com` será redirigido a tu app de Streamlit.

**Nota:** No es posible usar una subruta (`tudominio.com/calculadora`) para mostrar la app de Streamlit Cloud, solo subdominios o redirección directa.

---

## 🔒 Seguridad

### Información Protegida:
- ✅ No hay contraseñas en el código
- ✅ No hay claves API públicas
- ✅ Repositorio puede ser privado
- ✅ Solo la app es pública, no el código

### Archivos Excluidos (.gitignore):
- Variables de entorno (`.env`)
- Archivos de respaldo
- Cache de Python
- Configuraciones locales

## 🔄 Actualizaciones

Para actualizar la app desplegada:

```bash
# Hacer cambios en tu código local
git add .
git commit -m "Descripción de los cambios"
git push origin main
```

Streamlit Cloud detectará los cambios automáticamente y redesplegará la app.

## 📞 Soporte

Si tienes problemas con el despliegue:
- Revisa los logs en Streamlit Cloud
- Verifica que todas las dependencias estén en `requirements.txt`
- Asegúrate de que las rutas de archivos sean relativas

## ✅ Checklist Final

Antes de desplegar, verifica:
- [ ] La app funciona correctamente en local
- [ ] No hay warnings ni errores en consola
- [ ] Todas las imágenes se cargan
- [ ] El CSS se aplica correctamente
- [ ] Los cálculos son precisos
- [ ] El footer se visualiza bien
- [ ] El README es claro y profesional
- [ ] requirements.txt está actualizado

---

**Última actualización**: Febrero 2026
**Versión**: 1.0.0
