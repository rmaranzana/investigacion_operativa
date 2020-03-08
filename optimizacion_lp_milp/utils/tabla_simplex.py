from plotly import graph_objs as go
from copy import deepcopy as copy
import numpy as np
np.set_printoptions(edgeitems=30, linewidth=100000,
    formatter=dict(float=lambda x: "%.3g" % x))


class TablaSIMPLEX:
    def __init__(self, variables, costo, len_base):
        self.costo = costo
        self.variables = variables
        self.len_base = len_base
        self.estructura = self.__construir_template()
        self.submatrix = self.actualizar_submatrix()

    def actualizar_submatrix(self):
        self.submatrix = self.estructura._data_objs[0].cells  # Referencia a atributos de tabla

    def copiar_tabla(self):
        copia = copy(self)
        copia.actualizar_submatrix()

        return copia

    def __construir_template(self):
        variables = self.variables
        costo = self.costo
        len_base = self.len_base

        # Construir columnas:
        header_values = ["", "", '$C_j$'] + costo
        col_i = ['$C_j base$'] + [0] * len_base + [''] + [0]
        col_ii = ['$Var. Base$'] + [''] * len_base
        col_iii = ['$B_k$'] + [0] * len_base + ['$z_j$', '$z_j - c_j$']
        rest_cols = [[variable] + [0] * (len_base + 2) for variable in variables]

        cells_values = [col_i, col_ii, col_iii] + rest_cols + [['$Bk/A_{ij}$'] + [0] * len_base]

        # Color base:
        color = np.chararray((len(cells_values[0]), len(cells_values)), itemsize=6, unicode=True)
        color[:] = 'white'

        # Construir y printear tabla:
        layout = go.Layout(height=250,
                           margin=go.layout.Margin(l=25, r=25, b=0, t=25, pad=0),
                           autosize=False)
        fig = go.Figure(data=[go.Table(header=dict(values=header_values),
                                       cells=dict(values=cells_values,
                                                  fill=dict(color=color.tolist())))],
                        layout=layout)

        return fig

    def actualizar_A_zj_zjcj(self, Aij, zj, zj_cj):
        Aij_t = Aij.transpose()
        Aij_t = [[f'{i:.2f}' for i in j] for j in Aij_t] if Aij.dtype == float else Aij_t.tolist()

        for j in range(0, len(self.variables)):
            # Actualizar A:
            self.submatrix.values[j+3][1:(1+self.len_base)] = Aij_t[j]

            # Actualizar zj:
            self.submatrix.values[j+3][self.len_base+1] = f'{zj[j]:.2f}'

            # Actualizar zj_cj:
            self.submatrix.values[j+3][self.len_base+2] = f'{zj_cj[j]:.2f}'

    def actualizar_b(self, b):
        self.submatrix.values[2][1:self.len_base+1] = [f'{i:.2f}' for i in b] if (b.dtype == float) else b.tolist()

    def actualizar_bk_Aij(self, bk_Aij):
        self.submatrix.values[-1][1:self.len_base+1] = [f'{i:.2f}' for i in bk_Aij] if (bk_Aij.dtype == float) else bk_Aij.tolist()

    def actualizar_base(self, base):
        # Actualizar variables base:
        self.submatrix.values[1][1:self.len_base+1] = [self.variables[i] for i in base]

        # Actualizar c base:
        self.submatrix.values[0][1:self.len_base+1] = [self.costo[i] for i in base]

    def actualizar_costo(self, costo):
        self.submatrix.values[0][self.len_base + 2] = f'{costo:.2f}'

    def actualizar_pivote(self, pivote):
        # Color base:
        color = np.chararray((len(self.submatrix.fill.color), len(self.submatrix.fill.color[0])), itemsize=6, unicode=True)
        color[:] = 'white' # TEMPORAL

        color[pivote[0] + 1, :] = 'yellow'
        color[:, pivote[1] + 3] = 'yellow'

        color = color.transpose()

        # Reemplazar color:
        self.submatrix.fill.color = color.tolist()


class ConstructorTablasSIMPLEX:
    def __init__(self, variables, costo, len_base):
        self.template = TablaSIMPLEX(variables, costo, len_base)

    def crear_nueva_tabla(self, base, b, A, zj, zj_cj, bk_Aij, costo_tot, pivote):
        nueva_tabla = self.template.copiar_tabla()

        nueva_tabla.actualizar_A_zj_zjcj(A, zj, zj_cj)
        nueva_tabla.actualizar_b(b)
        nueva_tabla.actualizar_bk_Aij(bk_Aij)
        nueva_tabla.actualizar_base(base)
        nueva_tabla.actualizar_costo(costo_tot)
        nueva_tabla.actualizar_pivote(pivote) if pivote != None else None

        return nueva_tabla

    def construir_print_nueva_tabla(self, base, b, A, zj, zj_cj, bk_Aij, costo_tot, pivote):
        nueva_tabla = self.crear_nueva_tabla(base, b, A, zj, zj_cj, bk_Aij, costo_tot, pivote)

        nueva_tabla.estructura.show()


if __name__ == '__main__':
    ## Datos de entrada:
    variables = ['$X_1$', '$X_2$', '$X_3$', '$X_4$', '$X_5$', '$X_6$']

    c = [1000, 1200, 0, 0, 0, 0]  # Coeficientes de funcion objetivo

    A = [[10, 5, 1, 0, 0, 0],
         [2, 3, 0, 1, 0, 0],
         [1, 0, 0, 0, 1, 0],
         [0, 1, 0, 0, 0, 1]]  # Coeficientes tecnológicos

    b = [200, 60, 34, 14]  # Término LHS

    base = [2, 3, 4, 5]


    constructor = ConstructorTablasSIMPLEX(variables,
                                           c,
                                           len(base))

    constructor.crear_nueva_tabla(base,
                                  np.array(b),
                                  np.array(A),
                                  np.array([0, 0, 0, 0, 0, 0]),
                                  np.array([-1000, -1200, 0, 0, 0, 0]),
                                  np.array([40, 20, np.Inf, 14]),
                                  0,
                                  (3, 1))