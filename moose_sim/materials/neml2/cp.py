"""
 Title:         Isotropic Elasticity in NEML2
 Description:   For creating the material file;
                Based on moose/modules/solid_mechanics/test/tests/neml2/models/elasticity.i
 Author:        Janzen Choi

"""

# Libraries
from moose_sim.materials.__material__ import __Material__

# Format for defining materials
MATERIAL_FORMAT = """
[Models]
  [{material_name}]
    type = LinearIsotropicElasticity
    youngs_modulus = {youngs}
    poisson_ratio = {poissons}
    strain = "state/elastic_strain"
    stress = "state/internal/cauchy_stress"
  []
[]
"""

# VSHAI Class
class Material(__Material__):
    
    def get_material(self, youngs:float, poissons:float) -> str:
        """
        Gets the content for the material file;
        must be overridden
        
        Parameters:
        * `youngs`:   The elastic modulus
        * `poissons`: The poisson ratio
        """
        material_content = MATERIAL_FORMAT.format(
            material_name = self.get_name(),
            youngs        = youngs,
            poissons      = poissons,
        )
        return material_content
    