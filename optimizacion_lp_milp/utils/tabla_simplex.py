import numpy as np
from plotly import graph_objs as go

def fijar_decimales_array(array):
    return [f'{i:.2f}' for i in array] if (array.dtype == float) else array.tolist()


def visualizar_tabla(variables, base, cj, bk, Aij, zj, zj_cj, bk_aij, costo_total, pivote):
    Aij_t = Aij.transpose()
    Aij_t = [[f'{i:.2f}' for i in j] for j in Aij_t] if Aij.dtype == float else Aij_t.tolist()

    cj = fijar_decimales_array(cj)
    bk = fijar_decimales_array(bk)
    zj = fijar_decimales_array(zj)
    zj_cj = fijar_decimales_array(zj_cj)
    bk_aij = fijar_decimales_array(bk_aij)
    costo_total = f'{costo_total:.2f}'

    # Construir columnas:
    header_values = ['', '', '$C_j$'] + cj
    col_i = ['$C_j base$'] + [cj[i] for i in base] + [''] + [costo_total]
    col_ii = ['$Var. Base$'] + [variables[i] for i in base]
    col_iii = ['$B_k$'] + bk + ['$z_j$', '$z_j - c_j$']
    rest_cols = [[variables[i]] + col + [zj[i]] + [zj_cj[i]] for i, col in enumerate(Aij_t)]

    cells_values = [col_i, col_ii, col_iii] + rest_cols + [['$Bk/A_{ij}$'] + bk_aij]

    # Colorear columna pivote:
    color = np.chararray((len(cells_values[0]), len(cells_values)), itemsize=6, unicode=True)
    color[:] = 'white'

    if pivote != None:
        color[pivote[0] + 1, :] = 'yellow'
        color[:, pivote[1] + 3] = 'yellow'

    # Construir y printear tabla:
    layout = go.Layout(height=250,
                       margin=go.layout.Margin(l=25, r=25, b=0, t=25, pad=0),
                       autosize=False)
    fig = go.Figure(data=[go.Table(header=dict(values=header_values),
                                   cells=dict(values=cells_values,
                                              fill=dict(color=color.tolist())))],
                    layout=layout)

    fig.show()
