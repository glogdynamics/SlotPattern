import ezdxf

def create_dxf(file_name):
    # Tworzenie nowego dokumentu DXF
    doc = ezdxf.new(dxfversion='R2010')

    # Dodanie warstwy do dokumentu
    doc.layers.add(name='MyLayer', color=7)  # Kolor biały

    # Uzyskanie modelspace, aby dodać do niego elementy
    msp = doc.modelspace()

    # Dodanie linii do modelspace
    msp.add_line((0, 0), (10, 0), dxfattribs={'layer': 'MyLayer'})
    msp.add_line((10, 0), (10, 10), dxfattribs={'layer': 'MyLayer'})
    msp.add_line((10, 10), (0, 10), dxfattribs={'layer': 'MyLayer'})
    msp.add_line((0, 10), (0, 0), dxfattribs={'layer': 'MyLayer'})
    msp.add_arc(radius=5, center=(0, 0), start_angle=15, end_angle=130)

    # Dodanie tekstu do modelspace
    msp.add_text("Hello DXF", dxfattribs={
        'layer': 'MyLayer',
        'height': 0.5
    })
    #.set_pos((5, 5), align='MIDDLE_CENTER')

    # Zapisanie pliku DXF
    doc.saveas(file_name)
    print(f'Plik DXF zapisany jako {file_name}')

# Użycie funkcji do stworzenia i zapisania pliku DXF
create_dxf('example.dxf')
