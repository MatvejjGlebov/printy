import streamlit as st
import trimesh
import matplotlib.pyplot as plt
import tempfile
import os

# Заголовок приложения
st.title("STL Model Viewer и Калькулятор Стоимости")

# Загрузка STL-файла
uploaded_file = st.file_uploader("Выберите STL-файл", type="stl")

if uploaded_file is not None:
    # Сохраняем файл во временное хранилище
    with tempfile.NamedTemporaryFile(delete=False, suffix='.stl') as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    try:
        # Загрузка модели
        your_mesh = trimesh.load(tmp_file_path)

        # Получение границ модели и расчет габаритов
        min_coords, max_coords = your_mesh.bounds
        dimensions = max_coords - min_coords

        # Расчет объема
        volume = your_mesh.volume  # в мм³

        # Визуализация 3D модели
        fig_3d = plt.figure()
        axes_3d = fig_3d.add_subplot(111, projection='3d')
        axes_3d.plot_trisurf(
            your_mesh.vertices[:, 0],
            your_mesh.vertices[:, 1],
            your_mesh.vertices[:, 2],
            triangles=your_mesh.faces,
            shade=True,
            color='cyan'
        )
        axes_3d.set_xlim(min_coords[0], max_coords[0])
        axes_3d.set_ylim(min_coords[1], max_coords[1])
        axes_3d.set_zlim(min_coords[2], max_coords[2])
        axes_3d.set_xlabel('X')
        axes_3d.set_ylabel('Y')
        axes_3d.set_zlabel('Z')

        st.pyplot(fig_3d)

        # Визуализация 2D проекций
        fig_projections, axes_projections = plt.subplots(1, 3, figsize=(15, 5))
        axes_projections[0].scatter(your_mesh.vertices[:, 0], your_mesh.vertices[:, 1], color='blue')
        axes_projections[0].set_title('XY проекция')
        axes_projections[0].set_xlabel('X')
        axes_projections[0].set_ylabel('Y')

        axes_projections[1].scatter(your_mesh.vertices[:, 1], your_mesh.vertices[:, 2], color='green')
        axes_projections[1].set_title('YZ проекция')
        axes_projections[1].set_xlabel('Y')
        axes_projections[1].set_ylabel('Z')

        axes_projections[2].scatter(your_mesh.vertices[:, 0], your_mesh.vertices[:, 2], color='red')
        axes_projections[2].set_title('XZ проекция')
        axes_projections[2].set_xlabel('X')
        axes_projections[2].set_ylabel('Z')

        st.pyplot(fig_projections)

        # Вывод габаритов и объема
        st.write(f"Габариты модели (мм): X: {dimensions[0]:.2f}, Y: {dimensions[1]:.2f}, Z: {dimensions[2]:.2f}")
        st.write(f"Объем модели: {volume:.2f} мм³")

        # Блок ввода данных для расчета стоимости
        st.subheader("Расчет стоимости печати")
        cost_mat = st.text_input('Стоимость катушки/банки материала (руб):')
        st.write('Для Григория: 1 ЛИТР = 1000000(10ˆ6) ммˆ3')
        volume_mat = st.text_input('Объем материала (мм³):')

        if cost_mat and volume_mat:
            try:
                cost_mat = float(cost_mat)
                volume_mat = float(volume_mat)
                price_fig = cost_mat / volume_mat * volume
                st.success(f'Ориентировочная стоимость модели: {price_fig:.2f} руб.')
            except ValueError:
                st.error("Пожалуйста, введите корректные числовые значения.")
    finally:
        # Очистка временного файла
        os.unlink(tmp_file_path)
