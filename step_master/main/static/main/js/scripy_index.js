const swiper = new Swiper('.swiper', {
  pagination: {
    el: ".swiper-pagination",
  },
});


document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('order-form');
  const messageDiv = document.getElementById('form-message');

  form.addEventListener('submit', async function (event) {
      event.preventDefault(); // Отменить стандартное поведение формы

      // Собрать данные из формы
      const formData = new FormData(form);

      try {
          const response = await fetch(form.action, {
              method: 'POST',
              body: formData,
              headers: {
                  'X-Requested-With': 'XMLHttpRequest' // Указать, что это AJAX-запрос
              }
          });

          if (response.ok) {
              const data = await response.json(); // Обработать ответ
              if (data.success) {
                  messageDiv.textContent = 'Заказ успешно оформлен!';
                  messageDiv.style.color = 'green';
                  messageDiv.style.display = 'block';

                  // Очистить форму
                  form.reset();
              } else {
                  messageDiv.textContent = 'Произошла ошибка при оформлении заказа.';
                  messageDiv.style.color = 'red';
                  messageDiv.style.display = 'block';
              }
          } else {
              throw new Error('Ошибка сервера');
          }
      } catch (error) {
          messageDiv.textContent = 'Не удалось отправить заказ. Попробуйте позже.';
          messageDiv.style.color = 'red';
          messageDiv.style.display = 'block';
      }
  });
});