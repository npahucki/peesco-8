//
//  ViewController.m
//  BartendroPad
//
//  Created by Pablo Castro on 12/3/13.
//  Copyright (c) 2013 witty. All rights reserved.
//

#import "DrinkListViewController.h"

@interface DrinkListViewController () < UITextFieldDelegate,
                                        UICollectionViewDataSource,
                                        UICollectionViewDelegateFlowLayout>

@property (strong, nonatomic) NSMutableArray * topDrinkList;
@property (strong, nonatomic) NSMutableArray * otherDrinkList;

@property (strong, nonatomic) IBOutlet UICollectionView * DrinksMenu;

@end

@implementation DrinkListViewController

- (void)viewDidLoad
{
    [super viewDidLoad];
    
    [self getDrinkList];

}



-(void) getDrinkList{
    
    AFHTTPRequestOperationManager * manager = [AFHTTPRequestOperationManager manager];
    
    [manager GET:@"http://192.168.2.16/ws/drink/dindex"
      parameters:nil
     
         success:^(AFHTTPRequestOperation *operation, id responseObject) {
             NSLog(@"JSON: %@", responseObject);
             
             NSArray * td = [[[responseObject objectForKey:@"AllDrinks"] objectAtIndex:0] objectForKey:@"topDrinks"];
             NSArray * od = [[[responseObject objectForKey:@"AllDrinks"] objectAtIndex:1] objectForKey:@"otherDrinks"];
             
             //             NSLog(@"top drinks  : %@", td);
             //             NSLog(@"Other drinks  : %@", td);
             
             
             [self fillTopDrinkListFromJSON:td];
             [self fillOtherDrinkListFromJSON:od];
             
             
         }
     
         failure:^(AFHTTPRequestOperation *operation, NSError *error) {
             NSLog(@"Error: %@", error);
         }
     ];



}


- (void) fillTopDrinkListFromJSON:(NSArray *) jsonList{

    self.topDrinkList = [[NSMutableArray alloc] init];
    
    for (NSDictionary * dict in jsonList){
        
        //NSLog(@"dict: %@", dict);
        
        Drink * d = [[Drink alloc] init];
        [d fillWithAttributes:dict];
        [self.topDrinkList addObject:d];
    }
    
    NSLog(@"We have %d Top drinks", [self.topDrinkList count]);
    [self.DrinksMenu reloadData];
    
}


- (void) fillOtherDrinkListFromJSON:(NSArray *) jsonList{
    
    
    self.otherDrinkList = [[NSMutableArray alloc] init];
    
    for (NSDictionary * dict in jsonList){
        
        //NSLog(@"dict: %@", dict);
        
        Drink * d = [[Drink alloc] init];
        [d fillWithAttributes:dict];
        [self.otherDrinkList addObject:d];
    }
    
    NSLog(@"We have %d other drinks", [self.otherDrinkList count]);
    [self.DrinksMenu reloadData];
    
}


- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

#pragma mark - UICollectionView Datasource

- (NSInteger)collectionView:(UICollectionView *)view numberOfItemsInSection:(NSInteger)section {
//    NSString *searchTerm = self.searches[section];
//    return [self.searchResults[searchTerm] count];

    
    NSLog(@"Section: %d", section);
    NSLog(@"topDrinkList: %d", [self.topDrinkList count]);
    NSLog(@"otherDrinkList: %d", [self.otherDrinkList count]);
    
    NSInteger retvalue = 0;
    
    switch (section) {
        case 0:
            
           retvalue = [self.topDrinkList count];
            
            break;
        case 1:
            retvalue = [self.otherDrinkList count];
            break;
            
        default:
            retvalue = 0;
            break;
    }
    
    NSLog(@"Drinks %d para la section %d", retvalue, section);
    
    
    return retvalue;
}

- (NSInteger)numberOfSectionsInCollectionView: (UICollectionView *)collectionView {
//    return [self.searches count];
    return 2;
}

- (UICollectionViewCell *)collectionView:(UICollectionView *)cv
                  cellForItemAtIndexPath:(NSIndexPath *)indexPath {
    
    DrinkCollectionViewCell * cell = [cv dequeueReusableCellWithReuseIdentifier:@"DrinkCell"
                                                                   forIndexPath:indexPath];
    
    Drink * d;
    
    NSLog(@"La row: %d", indexPath.row);
    NSLog(@"La seccion: %d", indexPath.section);
    
    switch (indexPath.section) {
        case 0:
            d = [self.topDrinkList objectAtIndex:indexPath.row];
            break;
            
        case 1:
            d = [self.otherDrinkList objectAtIndex:indexPath.row];
            break;
            
        default:
            break;
    }
    
    [cell populateUIwithDatafrom:d];
    
    return cell;
}


//- (UICollectionReusableView *)collectionView:
// (UICollectionView *)collectionView viewForSupplementaryElementOfKind:(NSString *)kind atIndexPath:(NSIndexPath *)indexPath
// {
// return [[UICollectionReusableView alloc] init];
//}



- (UICollectionReusableView *)collectionView:(UICollectionView *)collectionView viewForSupplementaryElementOfKind:(NSString *)kind atIndexPath:(NSIndexPath *)indexPath
{
    UICollectionReusableView *reusableview = nil;
    
    if (kind == UICollectionElementKindSectionHeader) {
        
        HeaderCollectionReusableView *headerView = [collectionView dequeueReusableSupplementaryViewOfKind:UICollectionElementKindSectionHeader withReuseIdentifier:@"HeaderView" forIndexPath:indexPath];
        
        NSString *title;
        
        
        if (indexPath.section == 0) {
                title = [[NSString alloc] initWithFormat:@"Lo tipico"];
        }
        
        if (indexPath.section == 1) {
            title = [[NSString alloc] initWithFormat:@"Lo Esencial"];
        }
        
        headerView.tituloHeader.text = title;
        
        reusableview = headerView;
    }
    
    
    return reusableview;
}

#pragma mark - UICollectionViewDelegate

- (void)collectionView:(UICollectionView *)collectionView didSelectItemAtIndexPath:(NSIndexPath *)indexPath
{
    // TODO: Select Item
}

- (void)collectionView:(UICollectionView *)collectionView didDeselectItemAtIndexPath:(NSIndexPath *)indexPath {
    // TODO: Deselect item
}















@end
